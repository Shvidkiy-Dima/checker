import React from "react";
import { Link, useParams } from "react-router-dom";
import { Layout, Col, Row, Descriptions, PageHeader } from "antd";
import {
  CheckCircleTwoTone,
  ClockCircleOutlined,
} from "@ant-design/icons";
import "../dashboard/dashboard.css";
import NotFound from "./not_found";
import Bar from "./bar";
import { Card, List, Table} from "antd";
import {getMonitorAction} from "../../store/actions/monitor";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "../../store/rootReducer";
import { Line } from "@ant-design/charts";
import { ColumnsType } from 'antd/es/table';


const TableColumns: ColumnsType<any> = [
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


export default function DetailMonitor() {
  const dispatch = useDispatch()
  const monitor = useSelector((state: RootState) => state.monitor)
  let { monitorId }: {monitorId: string} = useParams();


  console.log(monitor.chart_data)
  function getMonitor(){
      dispatch(getMonitorAction(monitorId))

  }

  React.useEffect(getMonitor, []);

  if (monitor.not_found) {
    return <NotFound />;
  }

  if (!monitor.loaded) {
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

      <Col span={24}>
          <Card bordered={false}>
                  <Row>
            <Col span={24} style={{fontSize: '2rem', textAlign: 'center'}}>
            <ClockCircleOutlined /> Scale
            </Col>
            <Col span={24}>
                {monitor.last_log ? <Bar monitor={monitor}/>: <div>Not data</div>}
            </Col>
          </Row>
          </Card>
      </Col>

      <Col span={24}>
          <Card title="Last 24 hours response time" bordered={false}>
            <Line {...monitor.chart_data} />
            </Card>
          </Col>

          <Col span={24}>
            <hr/>
            <h2>Last 24h error logs</h2>
            <Table columns={TableColumns} dataSource={monitor.table_data}/>
          </Col>

а
    </Row>
      </Layout.Content>
    </div>
  );
}
