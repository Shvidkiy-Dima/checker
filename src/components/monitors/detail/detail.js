 import React from "react";
import { Link, useParams } from "react-router-dom";
import { Layout, Col, Row, Descriptions } from "antd";
import "../monitor.css";
import request from "../../../utils/request";
import NotFound from "./not_found";
import { Line } from "@ant-design/charts";
import { DoubleLeftOutlined } from "@ant-design/icons";
import Bar from "../bar";
import convert_for_bar from "../../../utils/methods";
import Moment from "react-moment";

export default function DetailMonitor() {
  const [monitor, setMonitor] = React.useState(null);
  const [NotFoundError, setNotFoundError] = React.useState(false);
  const [BarMonitor, SetBarMonitor] = React.useState([]);
  const [config, setConfig] = React.useState(null);
  let { monitorId } = useParams();

  function getMonitor() {
    request(
      { url: "api/monitor/" + monitorId + "/", method: "get" },
      (res) => {
        setMonitor(res.data);
        SetBarMonitor(
          convert_for_bar(res.data.last_requests, res.data.interval)
        );
        let data = [];
        res.data.last_requests.forEach((i) => {
          data.push({ date: i.created, res_time: i.response_time });
        });
        setConfig({
          data,
          height: 400,
          xField: "date",
          yField: "res_time",
          point: { size: 1, shape: "diamond" },
        });
      },
      (err) => {
        setNotFoundError(true);
      }
    );
  }
  React.useEffect(getMonitor, []);

  if (NotFoundError) {
    return <NotFound />;
  }
  if (monitor === null || config === null) {
    return null;
  }

  return (
    <div>
      <Layout.Header className="site-layout-background" style={{ padding: 0 }}>
        <Link to="/dashboard">
          {" "}
          <DoubleLeftOutlined
            style={{ fontSize: "2em", marginRight: "10%" }}
          />{" "}
        </Link>
      </Layout.Header>
      <Layout.Content
        className="site-layout-background"
        style={{
          margin: "24px 16px",
          padding: 24,
          minHeight: 280,
        }}
      >
        <Row gutter={16}>
          <Col span={24}>
          Last 24 hours monitoring
          </Col>
          <Col span={16}>
            <Bar readings={BarMonitor} monitor={monitor} />
          </Col>
          <Col span={8}>
            <Descriptions layout="vertical">
              <Descriptions.Item label="Interval">
                {monitor.interval}
              </Descriptions.Item>
              <Descriptions.Item label="Created">
                <Moment format="MMMM Do YYYY, h:mm:ss a">
                  {monitor.created}
                </Moment>
              </Descriptions.Item>
            </Descriptions>
          </Col>
          <Col span={16}>
          <h3>Last 24 hours response time</h3>
            <Line {...config} />;
          </Col>
        </Row>
      </Layout.Content>
    </div>
  );
}
