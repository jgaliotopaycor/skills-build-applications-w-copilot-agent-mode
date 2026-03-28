import React, { useEffect, useState } from 'react';

export default function Users() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    setLoading(true);
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const protocol = window.location.protocol === 'https:' ? 'https' : 'http';
    const base = codespace ? `${protocol}://${codespace}-8000.app.github.dev` : '';
    const endpointPath = 'users';
    const url = `${base}/api/${endpointPath}/`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const list = data && data.results ? data.results : data;
        setItems(Array.isArray(list) ? list : []);
      })
      .catch((err) => console.error('Fetch error (Users):', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const headers = items && items.length > 0 && typeof items[0] === 'object'
    ? Object.keys(items[0])
    : [];

  return (
    <div className="card">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="h5 mb-0">Users</h2>
        <button className="btn btn-sm btn-outline-secondary" onClick={fetchData} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>
      <div className="card-body">
        {items.length === 0 ? (
          <div className="text-muted">No users found.</div>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-hover mb-0">
              <thead className="table-light">
                <tr>
                  {headers.map((h) => (
                    <th key={h}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {items.map((row, idx) => (
                  <tr key={idx}>
                    {headers.map((h) => (
                      <td key={h}>{typeof row[h] === 'object' ? JSON.stringify(row[h]) : String(row[h])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
