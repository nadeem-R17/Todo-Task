import React from "react";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import CameraIcon from "@mui/icons-material/Camera";
import { useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();
  const { username, password } = location.state || {};
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };
  return (
    <AppBar position="static" sx={{ px: 2, backgroundColor: "#00897B" }}>
      <Toolbar>
        <CameraIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          My App
        </Typography>
        {username && password ? (
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        ) : (
          <Button color="inherit">Login</Button>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
