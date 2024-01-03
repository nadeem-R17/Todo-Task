import React, { useState, useEffect } from "react";
import { Box, Typography, Collapse, Button } from "@mui/material";
import axios from "axios";
import { useLocation } from "react-router-dom";
import CreateButton from "./CreateButton";
import UpdateDialog from "./UpdateDialog";
import Grid from "@mui/material/Grid";

function Home() {
  const location = useLocation();
  const { username, password } = location.state;
  console.log(username);

  const [tasks, setTasks] = useState(null);
  const fetchTasks = () => {
    axios
      .get("https://todo12app.pythonanywhere.com/", {
        auth: {
          username: username,
          password: password,
        },
      })
      .then((res) => {
        setTasks(res.data);
        console.log(res.data);
      })
      .catch((error) => {
        console.log("This is the error ", error);
      });
  };

  useEffect(() => {
    fetchTasks();
  }, []);
  return (
    <div>
      <Grid container spacing={2}>
        {tasks &&
          tasks.map((task, index) => (
            <Grid item md={12} lg={6}>
              <TaskBox key={index} task={task} fetchTasks={fetchTasks} />
            </Grid>
          ))}
      </Grid>
      <CreateButton fetchTasks={fetchTasks} />
    </div>
  );
}

function TaskBox({ task, fetchTasks }) {
  const location = useLocation();
  const { username, password } = location.state;
  const handleDelete = () => {
    const token = btoa(`${username}:${password}`);

    axios
      .delete(`https://todo12app.pythonanywhere.com/${task.id}/delete/`, {
        headers: {
          Authorization: `Basic ${token}`,
        },
      })
      .then(() => {
        // Fetch tasks again to update the list
        fetchTasks();
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const [open, setOpen] = useState(false);

  const handleClick = () => {
    setOpen(!open);
  };

  const [openUpdateDialog, setOpenUpdateDialog] = useState(false);

  return (
    <Box
      sx={{
        width: "550px",
        maxWidth: "100%",
        minHeight: "100px",
        margin: "30px auto",
        backgroundColor: "#76D7C4", // softer color
        borderRadius: "10px",
        boxShadow: "0 10px 20px rgba(0, 0, 0, 0.1)",
        fontFamily: "Poppins, sans-serif",
        p: 2,
        "&:hover": {
          // hover effect
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)",
          cursor: "pointer",
        },
      }}
      onClick={handleClick}
    >
      <Typography
        sx={{ fontSize: "40px", fontFamily: "monospace", pt: 2, pb: 2 }}
      >
        {task.title}
      </Typography>
      <Collapse
        in={open}
        timeout={{
          enter: 500,
          exit: 250,
        }}
      >
        <Typography sx={{ mt: 2 }}>Description: {task.description}</Typography>

        <Typography sx={{ mt: 2 }}>Status: {task.status}</Typography>

        <Typography sx={{ mt: 2 }}>
          Due Date: {task.due_date ? task.due_date : "Not mentioned"}
        </Typography>

        <Typography sx={{ mt: 2 }}>
          Tags:
          {JSON.parse(task.tag.replace(/'/g, '"')).map((word, index, arr) => (
            <span key={index}>
              {word}
              {index < arr.length - 1 && ", "}
            </span>
          ))}
        </Typography>
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            alignItems: "flex-end",
          }}
        >
          <Button
            variant="contained"
            color="success"
            sx={{ mr: "6px" }}
            onClick={(event) => {
              event.stopPropagation();
              setOpenUpdateDialog(true);
            }}
          >
            Update
          </Button>
          {openUpdateDialog && (
            <UpdateDialog
              task={task}
              fetchTasks={fetchTasks}
              onClose={() => setOpenUpdateDialog(false)}
            />
          )}

          <Button
            variant="contained"
            color="error"
            onClick={(event) => {
              event.stopPropagation();
              handleDelete();
            }}
          >
            Delete
          </Button>
        </div>
      </Collapse>
    </Box>
  );
}

export default Home;
