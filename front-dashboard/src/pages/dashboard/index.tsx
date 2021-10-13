import React from "react";
import {useDispatch, useSelector} from "react-redux";
import {Button, Layout, Menu, Row} from "antd";
import {
  NodeExpandOutlined,
  LineChartOutlined,
  PlusOutlined,
  ImportOutlined
} from "@ant-design/icons";
import "./dashboard.css";
import {
  Link,
} from "react-router-dom";
import Monitors from "./components/monitors";
import {LogoutAction} from "../../store/actions/profile";
import {RootState} from "../../store/rootReducer";

const {Sider} = Layout;

export default function Dashboard() {

  const dispatch = useDispatch()
  const email = useSelector((state: RootState)=> state.profile.email)

  return (
    <Layout style={{height: '100%'}}>
      <Sider  breakpoint="lg" collapsedWidth="0" trigger={null}>
      <div style={{color: 'white'}}><img style={{marginLeft: '20%'}} className="logo" src="/assets/img/logo.png" /></div>
        <Menu
          style={{ marginTop: "50%" }}
          theme="dark"
          mode="inline"
          defaultSelectedKeys={["1"]}
        >
          <Menu.Item
            key="3"
            style={{ fontSize: "2em", marginTop: "20%" }}
            icon={<ImportOutlined style={{ fontSize: "0.8em" }} />}
            onClick={()=>dispatch(LogoutAction())}
          >
            Logout
          </Menu.Item>

          <Menu.Item
          style={{color: 'white', fontSize: '1rem'}}
          >
            {email}
          </Menu.Item>

        </Menu>
      </Sider>

      <Layout style={{ height: "100%", background: '#ebe4e4'}} className="site-layout">
        <Monitors/>
      </Layout>
    </Layout>
  );
}
