import React from "react";
import { Layout, Menu, Button, Modal, Slider, Form, Input } from "antd";
import {
  PlusOutlined,
} from "@ant-design/icons";
import "./monitor.css";
import request from "../../utils/request";
import Monitor from "./monitor";
import MonitorForm from "./form";

const { Header, Sider, Content } = Layout;

export default function DashBoard({ ws, logout, user }) {
  const [Monitors, SetMonitors] = React.useState(null);
  const [show, setShow] = React.useState(false);

  const handleShow = () => setShow(true);

  function GetMonirots() {
    request({ method: "get", url: "api/monitor/" }, (res) => {
      let data = {};
      res.data.forEach((monitor) => (data[monitor.id] = monitor));
      SetMonitors(data);
    });
  }

  function DeleteMonitor(monitor_id) {
    request(
      { url: "api/monitor/" + monitor_id + "/", method: "delete" },
      (res) => {
        delete Monitors[monitor_id];
        SetMonitors({ ...Monitors });
      },
      (err) => {
        console.log(err);
      }
    );
  }

  function GetChangesFromWS(data) {
    console.log("WS", data["data"]);
    let log = data["data"];
    SetMonitors({ ...Monitors, [log.monitor.id]: log.monitor });
  }

  React.useEffect(() => {
      ws.dispatch.refresh_monitors = GetChangesFromWS;
      return ()=>{ws.dispatch.refresh_monitors = null}
  });
  React.useEffect(GetMonirots, []);

  if (Monitors === null){
    return null
  }

  return (
    <Content
      className="site-layout-background"
      style={{
        margin: "24px 16px",
        padding: 24,
        minHeight: 280,
      }}
    >
      <MonitorForm
        show={show}
        setShow={setShow}
        SetMonitors={SetMonitors}
        Monitors={Monitors}
        user={user}
      />
      <div style={{ textAlign: "center", marginBottom: "2%" }}>
        <Button size="large" type="primary" onClick={handleShow} danger>
          <PlusOutlined />
          New monitor
        </Button>
      </div>
      {Object.entries(Monitors).map(([key, value]) => (
        <Monitor delete_monitor={DeleteMonitor} key={key} monitor={value} />
      ))}
    </Content>
  );
}