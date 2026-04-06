import { useEffect, useMemo, useState } from "react";
import api from "../api";

function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [titleDrafts, setTitleDrafts] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadTitle, setUploadTitle] = useState("");
  const [isBusy, setIsBusy] = useState(false);
  const [error, setError] = useState("");

  const totalChunks = useMemo(
    () => documents.reduce((sum, item) => sum + (item.chunk_count || 0), 0),
    [documents]
  );

  async function fetchDocuments() {
    const response = await api.get("/documents");
    setDocuments(response.data);

    const nextDrafts = {};
    response.data.forEach((item) => {
      nextDrafts[item.id] = item.title;
    });
    setTitleDrafts(nextDrafts);
  }

  async function uploadDocument(event) {
    event.preventDefault();
    if (!selectedFile) return;

    setIsBusy(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      if (uploadTitle.trim()) {
        formData.append("title", uploadTitle.trim());
      }
      await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSelectedFile(null);
      setUploadTitle("");
      await fetchDocuments();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Khong the upload tai lieu.");
    } finally {
      setIsBusy(false);
    }
  }

  async function saveTitle(documentId) {
    const title = (titleDrafts[documentId] || "").trim();
    if (!title) return;

    setIsBusy(true);
    setError("");
    try {
      await api.put(`/documents/${documentId}`, { title });
      await fetchDocuments();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Khong the cap nhat tieu de.");
    } finally {
      setIsBusy(false);
    }
  }

  async function embedDocument(documentId) {
    setIsBusy(true);
    setError("");
    try {
      await api.post(`/documents/${documentId}/embed`);
      await fetchDocuments();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Khong the embedding tai lieu.");
    } finally {
      setIsBusy(false);
    }
  }

  async function deleteDocument(documentId) {
    setIsBusy(true);
    setError("");
    try {
      await api.delete(`/documents/${documentId}`);
      await fetchDocuments();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Khong the xoa tai lieu.");
    } finally {
      setIsBusy(false);
    }
  }

  async function rebuildIndex() {
    setIsBusy(true);
    setError("");
    try {
      await api.post("/documents/reindex");
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Khong the rebuild index.");
    } finally {
      setIsBusy(false);
    }
  }

  useEffect(() => {
    fetchDocuments().catch(() => setError("Khong the tai danh sach tai lieu."));
  }, []);

  return (
    <div className="panel panel-main">
      <div className="panel-head">
        <h2>Quan li tai lieu</h2>
        <div className="panel-actions">
          <span className="muted">Tai lieu: {documents.length}</span>
          <span className="muted">Tong chunks: {totalChunks}</span>
          <button onClick={rebuildIndex} disabled={isBusy}>
            Rebuild index
          </button>
        </div>
      </div>

      <form className="upload-form" onSubmit={uploadDocument}>
        <input
          type="file"
          onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
          accept=".pdf,.txt,.md"
        />
        <input
          type="text"
          placeholder="Title (optional)"
          value={uploadTitle}
          onChange={(event) => setUploadTitle(event.target.value)}
        />
        <button type="submit" disabled={isBusy || !selectedFile}>
          {isBusy ? "Dang xu ly..." : "Upload"}
        </button>
      </form>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Tieu de</th>
              <th>File goc</th>
              <th>Status</th>
              <th>Chunks</th>
              <th>Hanh dong</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.id}</td>
                <td>
                  <input
                    value={titleDrafts[doc.id] || ""}
                    onChange={(event) =>
                      setTitleDrafts((prev) => ({ ...prev, [doc.id]: event.target.value }))
                    }
                  />
                </td>
                <td>{doc.original_filename}</td>
                <td>{doc.status}</td>
                <td>{doc.chunk_count}</td>
                <td className="row-actions">
                  <button onClick={() => saveTitle(doc.id)} disabled={isBusy}>
                    Save
                  </button>
                  <button onClick={() => embedDocument(doc.id)} disabled={isBusy}>
                    Embed
                  </button>
                  <button className="danger" onClick={() => deleteDocument(doc.id)} disabled={isBusy}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}

export default DocumentsPage;
