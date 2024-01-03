import React, { useState } from "react";
import { Typography, TextField, Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../AuthContext";

function Login() {
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);
  const [error, setError] = useState(null);
  const { setIsLoggedIn } = useAuth();
  // console.log(username);
  // console.log(password);
  const navigate = useNavigate();
  const handleSubmit = () => {
    axios
      .get("https://todo12app.pythonanywhere.com", {
        headers: {
          Authorization: "Basic " + btoa(username + ":" + password),
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        // If the request is successful, set the login state and navigate to Home
        setIsLoggedIn(true);
        navigate("/home", { state: { username, password } });
      })
      .catch((error) => {
        alert("wrong username or password");
        // If the request fails, show an error message
        if (error.response && error.response.status === 401) {
          setError("Invalid username or password");
        } else {
          setError("An error occurred");
        }
      });
  };
  return (
    <Box
      sx={{
        width: "400px",
        maxWidth: "100%",
        margin: "50px auto",
        backgroundColor: "#00897B",
        borderRadius: "10px",
        boxShadow: "0 10px 20px rgba(0, 0, 0, 0.1)",
        fontFamily: "Poppins, sans-serif",
        p: 2,
      }}
    >
      <Typography align="center" variant="h4" sx={{ py: 2, color: "white" }}>
        Login
      </Typography>
      <Box
        sx={{
          p: 2,
          backgroundColor: "white",
          borderRadius: "10px",
          fontFamily: "Poppins, sans-serif",
        }}
      >
        <TextField
          id="username"
          label="Username"
          variant="outlined"
          fullWidth
          sx={{ mb: 2 }}
          onChange={(e) => {
            setUsername(e.target.value);
          }}
        />
        <TextField
          id="password"
          label="Password"
          type="password"
          variant="outlined"
          fullWidth
          sx={{ mb: 2 }}
          onChange={(e) => {
            setPassword(e.target.value);
          }}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          sx={{
            py: 1,
            mt: 2,
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
            "&:hover": {
              backgroundColor: "deepskyblue",
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.3)",
            },
          }}
          onClick={handleSubmit}
        >
          Login
        </Button>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" align="center">
            Login to view Task
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}

export default Login;
