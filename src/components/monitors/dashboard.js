import React from "react";
import { Layout, Menu, Button, Modal, Slider, Form, Input } from "antd";
import {
  NodeExpandOutlined,
  LineChartOutlined,
  ImportOutlined,
  PlusOutlined,
} from "@ant-design/icons";
import "./monitor.css";
import request from "../../utils/request";
import Monitor from "./new_monitor";
import MonitorForm from './form'
import {
    HashRouter as Router,
    Switch,
    Link,
    Route,
    Redirect,
  } from "react-router-dom";



const { Header, Sider, Content } = Layout;

export default function DashBoard({ ws, logout }) {
  const [Monitors, SetMonitors] = React.useState({});
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
    console.log('WS', data["data"]);
    let log = data["data"];
    SetMonitors({ ...Monitors, [log.monitor.id]: log.monitor });
  }

  React.useEffect(() => {
    ws.dispatch.refresh_monitors = GetChangesFromWS;
  });
  React.useEffect(GetMonirots, []);

  return (
    <Layout style={{ height: "100%" }}>
      
      <MonitorForm show={show} setShow={setShow} SetMonitors={SetMonitors} Monitors={Monitors} />

      <Sider trigger={null} breakpoint="lg" collapsedWidth="0">
        <Menu
          style={{ marginTop: "50%" }}
          theme="dark"
          mode="inline"
          defaultSelectedKeys={["1"]}
        >
          <Menu.Item
            style={{ fontSize: "2em" }}
            key="1"
            icon={<LineChartOutlined style={{ fontSize: "0.8em" }} />}
          >
            <Link to="/dashbroad">Monitors</Link>
          </Menu.Item>
          <Menu.Item
            key="2"
            style={{ fontSize: "2em", marginTop: "20%" }}
            icon={<NodeExpandOutlined style={{ fontSize: "0.8em" }} />}
          >
            <Link to="/dashbroad/settings">Settings</Link>
          </Menu.Item>
          <Menu.Item
            key="3"
            style={{ fontSize: "2em", marginTop: "20%" }}
            icon={<ImportOutlined style={{ fontSize: "0.8em" }} />}
          >
            Logout
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout className="site-layout">
        <Content
          className="site-layout-background"
          style={{
            margin: "24px 16px",
            padding: 24,
            minHeight: 280,
          }}
        >
        <Switch>
            <Route exact path='/dashboard'>
            <h3>Please select a topic.</h3>
            </Route>
            <Route path='/dashboard}/:monitorId'>
            <Topic />
            </Route>
            <Route path='/dashboard}/settings'>
            <Topic />
            </Route>
      </Switch>

        </Content>
      </Layout>
    </Layout>
  );
}
