export function apiUrl(endpointPath) {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const envBackend = process.env.REACT_APP_BACKEND_URL;
  const protocol = window.location.protocol === 'https:' ? 'https' : 'http';

  let base = '';
  if (envBackend) {
    base = envBackend.replace(/\/$/, '');
  } else if (codespace) {
    base = `${protocol}://${codespace}-8000.app.github.dev`;
  } else {
    base = `${protocol}://localhost:8000`;
  }

  return `${base}/api/${endpointPath.replace(/^\/+|\/+$/g, '')}/`;
}
