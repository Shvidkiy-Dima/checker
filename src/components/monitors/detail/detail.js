import React from "react";
import { Link, useParams } from "react-router-dom";
import { Layout, Col, Row, Descriptions } from "antd";
import "../monitor.css";
import request from "../../../utils/request";
import NotFound from "./not_found";
import { Line } from "@ant-design/charts";
import Bar from "../bar";
import convert_for_bar from "../../../utils/methods";
import Moment from "react-moment";
import Moment_f from "moment";
import { Card, List, Progress} from "antd";

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
        let data = res.data.last_requests.map((i) => {
          return {
            date: Moment_f.utc(i.created).local().format("HH:mm:ss"),
            res_time: i.response_time,
          };
        });
        console.log(res.data.last_requests);
        console.log(data);
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
            <h1 style={{ fontSize: "1.5em" }}>{monitor.name}</h1>
          </Col>
          <Col span={24}>
            <h2>
              <Link to={monitor.url}>{monitor.url}</Link>
            </h2>
          </Col>
          <Col span={24}>Last 24 hours monitoring</Col>
          <Col span={16}>
            <Bar readings={BarMonitor} monitor={monitor} />
          </Col>


          </Row>
          <Row gutter={16}>
          <Col span={16}>
            <h3>Last 24 hours response time</h3>
            <Line {...config} />;
          </Col>
          <Col span={8}>
            <Row justify="center">
              <List>
                <List.Item>
                  <Card  title='Interval' bordered={false}>
                    {monitor.interval_in_minutes}min
                    </Card>
                </List.Item>
                <List.Item>
                  <Card title='Created' bordered={false}>{Moment_f.utc(monitor.created).local().format("Y/M/D HH:mm:ss")}</Card>
                </List.Item>
                <List.Item>
                  <Card title='Notifications' bordered={false}>Telegram</Card>
                </List.Item>
              </List>
            </Row>
          </Col>
          </Row>
      </Layout.Content>
    </div>
  );
}
