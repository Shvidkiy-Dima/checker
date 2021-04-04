import React from "react";
import { Redirect, Link } from "react-router-dom";
import { InputHook } from "../../utils/hooks";
import request from "../../utils/request";
import { Button } from "antd";
import { Layout, Menu, Breadcrumb } from "antd";
import "./main.css";
import ReactTypingEffect from "react-typing-effect";

const { Header, Content, Footer } = Layout;

export default function Main({ auth }) {

  if (auth === true){
    return <Redirect to="/dashboard" />
  }


  return (
        <Layout className="layout">
          <Header>
            <div className="logo" />
            <Menu theme="dark" mode="horizontal">
              <Menu.Item key="1">
                <Link to="/registration" style={{ fontSize: "1.4em" }}>
                  Registration
                </Link>
              </Menu.Item>
              <Menu.Item key="2">
                <Link to="/login" style={{ fontSize: "1.4em" }}>
                  Login
                </Link>
              </Menu.Item>
            </Menu>
          </Header>
          <Content>
            <div
              className="site-layout-content"
              style={{ textAlign: "center"}}
            >
              <div  style={{ marginTop: '7%'}} >
              <ReactTypingEffect
                text={["Stop anxiety", "And let me", "Watch instead of you"]}
                cursorRenderer={(cursor) => (
                  <h1 style={{ fontSize: "4em" }}>{cursor}</h1>
                )}
                displayTextRenderer={(text, i) => (
                  <h1
                    style={{
                      fontSize: "4em",
                      fontFamily: "Source Code Pro",
                      textTransform: "uppercase",
                    }}
                  >
                    {text}
                  </h1>
                )}
              />

              <h1 style={{ fontSize: "2em", marginTop: '3%'}}>
                Keep calm, we will do all stuff.
                <br />
                Uptime monitoring service for your buiseness.
              </h1>

              <Button danger size="large">
                <Link to="/registration"> Here we go! </Link>
              </Button>
              </div>
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>
            Ant Design ©2018 Created by Ant UED
          </Footer>
        </Layout>
  );
}
