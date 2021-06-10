import React from "react";
import { Redirect, Link } from "react-router-dom";
import { Button } from "antd";
import { Layout, Menu} from "antd";
import ReactTypingEffect from "react-typing-effect";
import "./main.css";


export default function Main({ auth }) {

  if (auth === true){
    return <Redirect to="/dashboard" />
  }


  return (
        <Layout style={{height: '100%'}} className="layout">
          <Layout.Header>
            <img className="logo" src="/assets/logo.png" />
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
          </Layout.Header>
          <Layout.Content>
            <div
              className="site-layout-content"
              style={{ textAlign: "center"}}
            >
              <div  style={{ marginTop: '7%'}} >
              <ReactTypingEffect
                text={["Start monitoring", "right here"]}
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
                <br />
                Uptime monitoring service for your buiseness.
              </h1>

              <Button danger type="primary" size="large" style={{fontSize: '1.5em'}}>
                {/* <Link to="/registration"> Here we go! </Link> */}
                <Link to="/login"> Here we go! </Link>
              </Button>
              </div>
            </div>
          </Layout.Content>
          <Layout.Footer style={{ textAlign: "center" }}>
            ©2021 Created by Shvidkiy Dmitriy
          </Layout.Footer>
        </Layout>
  );
}
