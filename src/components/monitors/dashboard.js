import React from "react";
import { Redirect } from "react-router-dom";
import request from "../../utils/request";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form";
import Monitor from "./monitor";


export default function DashBoard({ws, logout}) {
  const [Monitors, SetMonitors] = React.useState({});
  const [show, setShow] = React.useState(false);
  const [MonitorType, setMonitorType] = React.useState(null);
  const [interval, setInterval] = React.useState(5);
  const [url, setUrl] = React.useState("");
  const [name, setName] = React.useState("");

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function GetMonirots() {
    request({ method: "get", url: "api/monitor/" }, (res) => {
      let data = {}
      res.data.forEach((monitor)=>data[monitor.id]=monitor)
      SetMonitors(data);
    });
  }

  function handleSave() {
    let data = { monitor_type: MonitorType, 'interval': interval*60, name, url };
    request(
      { method: "post", url: "api/monitor/", data },
      (res) => {
        let monitor = res.data
        SetMonitors({...Monitors, [monitor.id]: monitor})
      },
      (err) => {
        console.log(err);
      }
    );
  }

  function GetChangesFromWS(data){
    console.log(data['data'])
    let log = data['data']
    SetMonitors({...Monitors, [log.monitor.id]: log.monitor})
  }


  React.useEffect(()=>{ws.dispatch.refresh_monitors = GetChangesFromWS})
  React.useEffect(GetMonirots, []);
  return (
    <div>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Modal heading</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <select
            onChange={(e) => {
              setMonitorType(e.target.value);
            }}
            class="form-select"
            aria-label="Default select example"
          >
            <option selected>Type</option>
            <option value="0">Http</option>
          </select>

          {MonitorType == 0 ? (
            <div>
              <InputGroup className="mb-3">
                <InputGroup.Prepend>
                  <InputGroup.Text id="inputGroup-sizing-default">
                    Url
                  </InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl
                  onChange={(e) => {
                    setUrl(e.target.value);
                  }}
                  aria-label="Default"
                  aria-describedby="inputGroup-sizing-default"
                />
              </InputGroup>

              <InputGroup className="mb-3">
                <InputGroup.Prepend>
                  <InputGroup.Text id="inputGroup-sizing-default">
                    Name
                  </InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl
                  onChange={(e) => {
                    setName(e.target.value);
                  }}
                  aria-label="Default"
                  aria-describedby="inputGroup-sizing-default"
                />
              </InputGroup>
              <Form.Group controlId="formBasicRange">
                <Form.Label>Interval</Form.Label>
                <Form.Control
                  type="range"
                  min="5"
                  max="60"
                  step="1"
                  value={interval}
                  onChange={(e) => {
                    setInterval(e.target.value);
                  }}
                /> <b>{interval}</b>
              </Form.Group>
            </div>
          ) : (
            ""
          )}
          {MonitorType == 1 ? <h1>Hi2</h1> : ""}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSave}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>

      <div class="container-fluid">
        <div class="row">
          <div class="col-3 p-3 text-white bg-dark" style={{ width: "280px" }}>
            <svg class="bi me-2" width="40" height="32"></svg>
            <Button variant="primary" onClick={handleShow}>
              Add new monitor +
            </Button>
            <hr />
            <ul class="nav nav-pills flex-column mb-auto">
              <li class="nav-item">
                <a href="#" class="nav-link active">
                  <svg class="bi me-2" width="16" height="16"></svg>
                  Dashboard
                </a>
              </li>
              <li>
                <a href="#" class="nav-link text-white">
                  <svg class="bi me-2" width="16" height="16"></svg>
                  Settings
                </a>
              </li>
            </ul>
            <hr />
          </div>

          <div class="col-sm">
            {Object.entries(Monitors).map(([key, value])=><Monitor key={key} monitor={value} />)}
          </div>
        </div>
      </div>
    </div>
  );
}
