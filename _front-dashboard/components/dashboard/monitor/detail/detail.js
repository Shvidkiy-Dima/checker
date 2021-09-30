import React from "react";
import { Link, useParams } from "react-router-dom";
import { Layout, Col, Row, Descriptions, PageHeader } from "antd";
import {
  CheckCircleTwoTone,
  ClockCircleOutlined,
} from "@ant-design/icons";
import "../monitor.css";
import request from "../../../utils/request";
import NotFound from "./not_found";
import { Line } from "@ant-design/charts";
import Bar from "../bar";
import convert_for_bar from "../../../utils/methods";
import Moment from "moment";
import { Card, List, Table} from "antd";

export default function DetailMonitor() {

  const [monitor, setMonitor] = React.useState(null);
  const [NotFoundError, setNotFoundError] = React.useState(false);
  const [BarMonitor, SetBarMonitor] = React.useState([]);
  const [config, setConfig] = React.useState(null);
  const [dataSource, SetDataSource] = React.useState(null);
  let { monitorId } = useParams();



  function getMonitor() {

    request(
      { url: "api/monitor/" + monitorId + "/", method: "get" },
      (res) => {
        setMonitor(res.data);
        SetBarMonitor(
          convert_for_bar(res.data.log_groups, res.data.interval)
        );
        let data = res.data.response_time_for_day.map((i) => {
          return {
            date: `${Moment.utc(i.start).local().format("HH:mm:ss")}-${Moment.utc(i.end).local().format("HH:mm:ss")}`,
            res_time: i.md,
          };
        });


        let error_logs = []
        
        res.data.last_error_logs.forEach((i, n)=>{
            error_logs.push({
                key: n,
                created: Moment.utc(i.created).local().format("MM.DD-HH:mm:ss"),
                error: i.error,
                res_code: i.response_code,
                res_time: i.response_time
            })
        })

        setConfig({
          data,
          height: 400,
          xField: "date",
          yField: "res_time",
          point: { size: 0.1, shape: "diamond" },
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


  const columns = [
    {
      title: 'Created',
      dataIndex: 'created',
      key: 'created',
    },
    {
      title: 'Error',
      dataIndex: 'error',
      key: 'error',
    },
    {
      title: 'Response code',
      dataIndex: 'res_code',
      key: 'res_code',
    },
    {
      title: 'Response time',
      dataIndex: 'res_time',
      key: 'res_time',
      responsive: ['md'],
    },
  ];


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

  <PageHeader
    className="site-page-header"
    title="Monitors"
    onBack={() => window.history.back()}
  />

  <Row  style={{background: 'white', marginBottom: 10}}>
    <Col span={24} style={{ fontSize: "1.5em", marginLeft: 20, marginTop: 5 }}>
    <h1><CheckCircleTwoTone twoToneColor="#52c41a" style={{marginRight: 10}}/>{monitor.name}</h1>
    </Col>
    <Col style={{marginLeft: 20}} span={24}>
    <h2>
    {monitor.url}
    </h2>
    </Col>
  </Row>

  <Row gutter={[16, 16]}>
      <Col xl={8} lg={12} md={12} sm={12} xs={24}>
        <Card bordered={false}>
          <Row>
            <Col span={24} style={{fontSize: '2rem', textAlign: 'center'}}>
            <ClockCircleOutlined /> Uptime
            </Col>
            <Col span={24} style={{fontSize: '1.5rem', textAlign: 'center'}}>
            {monitor.successful_percent}%
            </Col>
          </Row>
        </Card>
      </Col>
      <Col xl={8} lg={12} md={12} sm={12} xs={24}>
        <Card bordered={false}>
        <Row>
            <Col span={24} style={{fontSize: '2rem', textAlign: 'center'}}>
            <ClockCircleOutlined /> Avg. response time
            </Col>
            <Col span={24} style={{fontSize: '1.5rem', textAlign: 'center'}}>
            {monitor.avg_response_time} sec
            </Col>
          </Row>
        </Card>
      </Col>
      <Col xl={8} lg={12} md={12} sm={12} xs={24}>
        <Card bordered={false}>
          
        <Row>
            <Col span={24} style={{fontSize: '2rem', textAlign: 'center'}}>
            <ClockCircleOutlined /> interval
            </Col>
            <Col span={24} style={{fontSize: '1.5rem', textAlign: 'center'}}>
            Every {monitor.interval}
            </Col>
          </Row>


        </Card>
      </Col>
      <Col xl={8} lg={12} md={12} sm={12} xs={24}>
        <Card bordered={false}>
        
        <Row>
            <Col span={24} style={{fontSize: '2rem', textAlign: 'center'}}>
            <ClockCircleOutlined /> Last checked
            </Col>
            <Col span={24} style={{fontSize: '1.5rem', textAlign: 'center'}}>
            {monitor.last_request_in_seconds} sec ago
            </Col>
          </Row>

        </Card>
      </Col>
      <Col xl={8} lg={12} md={12} sm={12} xs={24}>
        <Card bordered={false}>

       

        <Row>
            <Col span={24} style={{fontSize: '2rem', textAlign: 'center'}}>
            <ClockCircleOutlined /> Scale
            </Col>
            <Col span={24}>
            <Bar readings={BarMonitor} monitor={monitor}/>
            </Col>
          </Row>

        </Card>


      </Col>


      <Col span={24}>
          <Card title="Last 24 hours response time" bordered={false}>
            <Line {...config} />
            </Card>
          </Col>

          <Col span={24}>
            <hr/>
            <h2>Last 24h error logs</h2>
            <Table columns={columns} dataSource={dataSource}/>
          </Col>


    </Row>
      </Layout.Content>
    </div>
  );
}
