import React, { useState } from "react";
import AddCircleRoundedIcon from "@mui/icons-material/AddCircleRounded";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
} from "@mui/material";
import { Button, Select, MenuItem } from "@mui/material";
import { useLocation } from "react-router-dom";
import axios from "axios";

function CreateButton(props) {
  const location = useLocation();
  const { username, password } = location.state;

  const [fontSize, setFontSize] = useState(60);

  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    due_date: "",
    tag: "",
    status: "OPEN",
  });
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleInputChange = (event) => {
    setForm({
      ...form,
      [event.target.id]: event.target.value,
    });
    console.log(event.target.value);
  };
  const handleInputStatus = (event) => {
    setForm({
      ...form,
      status: event.target.value,
    });
  };

  const handleSubmit = () => {
    const formCopy = { ...form };
    if (formCopy.due_date === "") {
      delete formCopy.due_date;
    }

    const formJson = JSON.stringify(formCopy);
    const token = btoa(`${username}:${password}`);
    axios
      .post("https://todo12app.pythonanywhere.com/create/", formJson, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Basic ${token}`,
        },
      })
      .then((response) => {
        console.log(response);
        props.fetchTasks();
      })
      .catch((error) => {
        console.error(error);
      });
    setForm({
      title: "",
      description: "",
      due_date: "",
      tag: "",
      status: "OPEN",
    });
    setOpen(false);
  };
  return (
    <div style={{ position: "fixed", bottom: "20px", right: "20px" }}>
      <AddCircleRoundedIcon
        className="create-button"
        style={{
          fontSize: fontSize,
          color: "green",
          transition: "font-size 0.3s ease",
        }}
        onMouseEnter={() => setFontSize(70)}
        onMouseLeave={() => setFontSize(60)}
        onClick={handleClickOpen}
      />
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Create a new Todo task</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="title"
            label="Title"
            type="text"
            fullWidth
            variant="standard"
            value={form.title}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            id="description"
            label="Description"
            type="text"
            fullWidth
            variant="standard"
            value={form.description}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            id="due_date"
            label="Due Date"
            type="date"
            fullWidth
            variant="standard"
            InputLabelProps={{
              shrink: true,
            }}
            value={form.due_date}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            id="tag"
            label="Tag"
            type="text"
            fullWidth
            variant="standard"
            value={form.tag}
            onChange={handleInputChange}
          />
          <Select
            labelId="status-label"
            id="status"
            value={form.status}
            label="Status"
            onChange={handleInputStatus}
          >
            <MenuItem value={"OPEN"}>OPEN</MenuItem>
            <MenuItem value={"DONE"}>DONE</MenuItem>
            <MenuItem value={"WORKING"}>WORKING</MenuItem>
            <MenuItem value={"OVERDUE"}>OVERDUE</MenuItem>
          </Select>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit}>Create</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default CreateButton;
