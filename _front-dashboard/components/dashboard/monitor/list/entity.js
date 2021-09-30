import React from "react";
import {
  Layout,
  Button,
  Card,
  Row,
  Col,
  Switch,
  Descriptions,
  Popover,
  Statistic,
  Divider,
  Dropdown,
  Menu,
} from "antd";
import {
  CheckCircleTwoTone,
  CloseOutlined,
  CloseCircleTwoTone,
  DownOutlined,
  EllipsisOutlined,
  MenuUnfoldOutlined,
  EditOutlined,
  PoweroffOutlined,
  InfoCircleOutlined
} from "@ant-design/icons";

import "./monitor.css";
import request from "../../utils/request";
import { Link } from "react-router-dom";
import Moment from "moment";

export default function Monitor({ monitor, delete_monitor }) {
  const [IsActive, SetIsAtive] = React.useState(monitor.is_active);

  function TurnOn(value) {
    request(
      {
        url: "api/monitor/" + monitor.id + "/",
        method: "patch",
        data: { is_active: value },
      },
      (res) => {
        SetIsAtive(res.data["is_active"]);
      },
      (err) => {
        console.log(err);
      }
    );
  }

  const menu = (
    <Menu>
      <Menu.Item>
        <Link to={"/dashboard/" + monitor.id} style={{ fontSize: "1em" }}>
          <MenuUnfoldOutlined />
          View
        </Link>
      </Menu.Item>
      <Menu.Item>
      <Link onClick={()=>{delete_monitor(monitor.id)}}>
          <CloseOutlined />
          Delete
        </Link>
      </Menu.Item>
      <Menu.Item>
      <Link onClick={()=>TurnOn(!IsActive)} style={{ fontSize: "1em" }}>
          <PoweroffOutlined />
          {IsActive ? 
          (<span>Disable</span>)
          : 
          (<span>Enable</span>)
          }
          
        </Link>
      </Menu.Item>
    </Menu>
  );

  return (
    <Col md={12} xs={24}>
      <Card
        title={<Link to={"/dashboard/" + monitor.id} style={{color: IsActive ? "#52c41a": '#9698ab'}}>{monitor.name}</Link>}
        bodyStyle={{ paddingTop: 0 }}
        bordered={true}
        headStyle={{
          border: 0,
          fontWeight: "bolder",
          fontSize: "2rem",
        }}
        extra={
          <Dropdown overlay={menu}>
            <a
              className="ant-dropdown-link"
              onClick={(e) => e.preventDefault()}
            >
              <EllipsisOutlined style={{ fontSize: 30 }} />
            </a>
          </Dropdown>
        }
      >
        <Row>
          <Col
            span={24}
            style={{
              textOverflow: "ellipsis",
              overflow: "hidden",
              whiteSpace: "nowrap",
            }}
          >

                <CheckCircleTwoTone
                  twoToneColor="#52c41a"
                  style={{ marginRight: 7 }}
                />

            {monitor.url}
          </Col>
          <Col span={24}>
            <Divider />
            <Row>
              <Col xl={12} lg={24} sm={24} md={24} xs={24}>
                <Row>
                  <Col span={12}>
                    <Row>
                      <Col span={24}>
                      <Popover
                            content={
                              <div>
                                <p>Based on last 24 hours {monitor.log_last_count} requests</p>
                              </div>
                            }
                        >                
                        Uptime <InfoCircleOutlined />
                        </Popover>
                        
                         </Col>
                        
                      <Col span={24} style={{ fontWeight: "bolder" }}>
                        {`${monitor.successful_percent}%`}
                      </Col>
                    </Row>
                  </Col>

                  <Col span={12}>
                    <Row>
                      <Col span={24}>
                      <Popover
                            content={
                              <div>
                                <p>Checked every {monitor.interval_in_minutes} min</p>
                              </div>
                            }
                        >     
                        Intervla <InfoCircleOutlined />
                        </Popover>
                        </Col>
                      <Col span={24} style={{ fontWeight: "bolder" }}>
                        Every {monitor.interval_in_minutes} min
                      </Col>
                    </Row>
                  </Col>
                </Row>
              </Col>

              <Col xl={12} lg={24} sm={24} md={24} xs={24}>
                <Row>
                  <Col span={12}>
                    <Row>
                      <Col span={24}>    
                        Last Checked
                        
                        </Col>
                      <Col span={24} style={{ fontWeight: "bolder" }}>
                          {monitor.last_request_in_seconds ? `${Moment.duration(monitor.last_request_in_seconds, "seconds").humanize()} ${"ago"}`: null}
                      </Col>
                    </Row>
                  </Col>
                  <Col span={12}>
                    <Row>
                      <Col span={24}>
                        Avg. response time
                        </Col>
                      <Col span={24} style={{ fontWeight: "bolder" }}>
                        {monitor.avg_response_time} sec
                      </Col>
                    </Row>
                  </Col>
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>
      </Card>
    </Col>
  );
}
