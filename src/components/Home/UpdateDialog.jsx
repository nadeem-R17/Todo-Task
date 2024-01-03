import { useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import axios from "axios";
import { useLocation } from "react-router-dom";

function UpdateDialog({ task, fetchTasks, onClose }) {
  const location = useLocation();
  const { username, password } = location.state;

  const [openDialog, setOpenDialog] = useState(true);
  const [currentTask, setCurrentTask] = useState(task);

  const [form, setForm] = useState({
    title: task.title,
    description: task.description,
    due_date: task.due_date,
    tag: task.tag,
    status: task.status,
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;

    setForm((prevForm) => ({
      ...prevForm,
      [name]: value,
    }));
  };

  const handleInputStatus = (event) => {
    const { value } = event.target;

    setForm((prevForm) => ({
      ...prevForm,
      status: value,
    }));
  };

  var str = "",
    temp = task.tag;
  var curr = true;
  for (let i = 0; i < temp.length; i++) {
    if (temp[i] === "'") {
      if (curr) {
        curr = !curr;
        continue;
      } else {
        str += " ";
        curr = !curr;
      }
    } else {
      if (!curr && (temp[i]!="[" || temp[i]!="]")) str += temp[i];
    }
  }

  const handleCloseDialog = () => {
    setOpenDialog(false);
    onClose();
  };

  const handleUpdate = () => {
    const formCopy = { ...form };
    if (formCopy.due_date === "") {
      delete formCopy.due_date;
    }

    const formJson = JSON.stringify(formCopy);
    const token = btoa(`${username}:${password}`);
    axios
      .patch(
        `https://todo12app.pythonanywhere.com/${task.id}/update/`,
        formJson,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Basic ${token}`,
          },
        }
      )
      .then((response) => {
        console.log(response);
        fetchTasks();
      })
      .catch((error) => {
        console.error(error);
      });
    console.log(formJson);
    handleCloseDialog();
  };

  return (
    <>
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Create a new Todo task</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="title"
            label="Title"
            type="text"
            fullWidth
            variant="standard"
            defaultValue={currentTask.title}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            name="description"
            label="Description"
            type="text"
            fullWidth
            variant="standard"
            defaultValue={currentTask.description}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            name="due_date"
            label="Due Date"
            type="date"
            fullWidth
            variant="standard"
            InputLabelProps={{
              shrink: true,
            }}
            defaultValue={currentTask.due_date}
            onChange={handleInputChange}
          />
          <TextField
            margin="dense"
            name="tag"
            label="Tag"
            type="text"
            fullWidth
            variant="standard"
            defaultValue={str}
            onChange={handleInputChange}
          />
          <Select
            labelId="status-label"
            name="status"
            defaultValue={currentTask.status}
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
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleUpdate}>Update</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default UpdateDialog;
