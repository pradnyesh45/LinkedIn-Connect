import { useState } from "react";
import {
  Container,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import axios from "axios";

function App() {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
    target_profile_url: "",
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        "http://localhost:8000/api/generate-message",
        credentials
      );
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          LinkedIn Message Generator
        </Typography>

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="LinkedIn Username"
            margin="normal"
            value={credentials.username}
            onChange={(e) =>
              setCredentials({
                ...credentials,
                username: e.target.value,
              })
            }
            required
          />

          <TextField
            fullWidth
            label="LinkedIn Password"
            type="password"
            margin="normal"
            value={credentials.password}
            onChange={(e) =>
              setCredentials({
                ...credentials,
                password: e.target.value,
              })
            }
            required
          />

          <TextField
            fullWidth
            label="Target Profile URL"
            margin="normal"
            value={credentials.target_profile_url}
            onChange={(e) =>
              setCredentials({
                ...credentials,
                target_profile_url: e.target.value,
              })
            }
            required
          />

          <Button
            variant="contained"
            type="submit"
            disabled={loading}
            sx={{ mt: 2 }}
          >
            {loading ? <CircularProgress size={24} /> : "Generate Message"}
          </Button>
        </form>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Paper sx={{ mt: 4, p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Generated Message:
            </Typography>
            <Typography paragraph>{result.message}</Typography>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Recent Posts:
            </Typography>
            {result.posts.map((post, index) => (
              <Paper key={index} sx={{ p: 2, mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  {post.timestamp}
                </Typography>
                <Typography>{post.content}</Typography>
              </Paper>
            ))}
          </Paper>
        )}
      </Paper>
    </Container>
  );
}

export default App;
