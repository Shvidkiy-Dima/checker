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
import Config from "./config/config";
import DetailMonitor from "./detail/detail";
import {
  HashRouter as Router,
  Switch,
  Link,
  Route,
  Redirect,
} from "react-router-dom";
import Monitors from './monitors'

const { Header, Sider, Content } = Layout;

export default function DashBoard({ ws, logout }) {
  return (
    <Layout style={{ height: "100%" }}>
        
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
            <Link to="/dashboard">Monitors</Link>
          </Menu.Item>
          <Menu.Item
            key="2"
            style={{ fontSize: "2em", marginTop: "20%" }}
            icon={<NodeExpandOutlined style={{ fontSize: "0.8em" }} />}
          >
            <Link to="/dashboard/settings">Settings</Link>
          </Menu.Item>
          <Menu.Item
            key="3"
            style={{ fontSize: "2em", marginTop: "20%" }}
            icon={<ImportOutlined style={{ fontSize: "0.8em" }} />}
            onClick={logout()}
          >
            Logout
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout className="site-layout">
          <Switch>

            <Route exact path="/dashboard/settings">
              <Config/>
            </Route>

            <Route path="/dashboard/:monitorId">
              <DetailMonitor/>
            </Route>


            <Route exact path="/dashboard">
              <Monitors ws={ws} logout={logout}/>
            </Route>

          </Switch>
      </Layout>
    </Layout>
  );
}
