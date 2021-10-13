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

import "../dashboard.css";
import { Link } from "react-router-dom";
import Moment from "moment";
import {useDispatch, useSelector} from "react-redux";
import {deleteMonitorAction, disableMonitorAction} from "../../../store/actions/dashboard";
import {IResponseMonitor} from "../../../interfaces/dashboard";

export default React.memo(function Monitor({monitor}: {monitor: IResponseMonitor}) {

  const dispatch = useDispatch()


    console.log('monitor', monitor.id)
  function DeleteMonitor() {
    dispatch(deleteMonitorAction(monitor.id))
  }


  function DisableMonitor() {
    dispatch(disableMonitorAction(monitor))
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
      <Button onClick={DeleteMonitor} type={'link'}>
          <CloseOutlined />
          Delete
        </Button>
      </Menu.Item>
      <Menu.Item>
      <Button onClick={DisableMonitor} type={'link'}>
          <PoweroffOutlined />
          {monitor.is_active ?
          (<span>Disable</span>)
          :
          (<span>Enable</span>)
          }

        </Button>
      </Menu.Item>
    </Menu>
  );

  return (
    <Col md={12} xs={24}>
      <Card
        title={<Link to={"/dashboard/" + monitor.id} style={{color: monitor.is_active ? "#52c41a": '#9698ab'}}>{monitor.name}</Link>}
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
                          {`${Moment.duration(monitor.last_request_in_seconds, "seconds").humanize()} ago`}
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
)