import React from "react";
import { Col, Layout, Menu,  notification, Row, Spin} from "antd";
import {
  NodeExpandOutlined,
  LineChartOutlined,
  ImportOutlined,
  DoubleLeftOutlined
} from "@ant-design/icons";
import "./monitor.css";
import Config from "./config/config";
import DetailMonitor from "./detail/detail";
import {
  HashRouter as Router,
  Switch,
  Link,
  Route,
  Redirect,
} from "react-router-dom";
import Monitors from "./monitors";
import RequireTelegram from './require_telegram'
import request from '../../utils/request'

const { Header, Sider, Content } = Layout;

export default function DashBoard({ ws, logout, user, setUser}) {

  // React.useEffect(()=>{

  //   if (!user.has_telegram){
  //     return
  //   }

  //     request({url: 'api/account/alert/', method: 'get'}, 
  //     (res)=>{
  //       let alerts = res.data.slice(0, 10)
  //       console.log(alerts)
  //       alerts.forEach(alert => {
  //         notification.info(
  //           {message: `Notification`,
  //           description: alert.msg,
  //           placement: 'topRight',
  //           onClose: ()=>{
  //             request({url: `api/account/alert/${alert.id}/`, method: 'patch'},
  //               (res)=>{},
  //               (err)=>{}
  //             )
  //           }
  //         });
  //       });

  //     },
  //     (err)=>{

  //     })
  // }, 
  // [])


  React.useEffect(()=>{

    if (user.has_telegram){
      return
    }

    const interval_id = setInterval(()=>{
      request(
        { method: "get", url: "api/account/profile/" },
        (res) => {
          if (res.data.has_telegram){
            clearInterval(interval_id);
            setUser(res.data);
          }
        },
        (err) => {
        }
      );

    }, 4000)


    return () => {
      clearInterval(interval_id);
  }

  },
  [])

  if (!user.has_telegram){

    return (
      <RequireTelegram/>
    )
  }


  return (
    <Layout style={{minHeight: '100%'}}>
      <Sider  breakpoint="lg" collapsedWidth="0" trigger={null}>
      <div style={{color: 'white'}}><img style={{marginLeft: '20%'}} className="logo" src="/assets/img/logo.png" /></div>
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
            onClick={logout}
          >
            Logout
          </Menu.Item>

          <Menu.Item
          style={{color: 'white', fontSize: '1rem'}}
          >
            {user.email}
          </Menu.Item>

        </Menu>
      </Sider>

      <Layout style={{ height: "100%", background: '#ebe4e4'}} className="site-layout">
        <Switch>
          <Route exact path="/dashboard/settings">
          <Layout.Header
              className="site-layout-background"
              style={{ padding: 0, textAlign: 'end'}}
              
            >
                <h2 style={{marginRight: '10%'}}>{user.email}</h2>
            </Layout.Header>
            <Config />
          </Route>

          <Route path="/dashboard/:monitorId">
            <DetailMonitor />
          </Route>

          <Route exact path="/dashboard">
            <Monitors ws={ws} logout={logout} user={user} />
          </Route>
        </Switch>
      </Layout>
    </Layout>
  );
}