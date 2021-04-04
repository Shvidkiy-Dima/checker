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
} from "antd";
import {
  CheckCircleTwoTone,
  CloseOutlined,
} from "@ant-design/icons";
import "./monitor.css";
import request from "../../utils/request";
import Bar from "./bar";
import Timer from './timer'


export default function Monitor({ monitor, delete_monitor }) {

  const [IsActive, SetIsAtive] = React.useState(monitor.is_active);
  const [BarMonitors, SetBarMonitor] = React.useState([]);

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

  function convert_for_bar(data, interval) {
    let step = null;
    if (interval === 1) {
      step = 1;
    }
    if (interval === 2) {
      step = 2;
    }

    if (step){
        for(var i = 0; i < data.length; i++) {
            data.splice(i+step,1);
        }
    }

    let new_data = data.map((e) => {
      return {
        name: e.created,
        value: 100 / data.length,
        color: e.error ? "#eb4d4b" : "green",
      };
    });

    return new_data;
  }

  React.useEffect(()=>{
    let new_monitors = convert_for_bar(monitor.last_requests, monitor.interval)
    SetBarMonitor(new_monitors)
  }, [monitor.log.created])


  return (
    <Card style={{ width: "100%" }}>
      <Row gutter={16}>
        <Col span={8} style={{ marginRight: "4%" }}>
          <h1>{ monitor.name } </h1>
          { monitor.url }
        </Col>
        <Col span={12}>
          <Descriptions layout="vertical">
            <Descriptions.Item label="Checked"><Timer monitor={monitor}/> </Descriptions.Item>
            <Descriptions.Item label="Last Response">
              {monitor.log.error ? (
              <Popover
                content={
                  <div>
                    <p>{monitor.log.error}</p>
                  </div>
                }
              >
                  <Button type="text" danger>Error: show</Button>
              </Popover>)
              : 
              (<Button type="text">{monitor.log.response_code} 
              {monitor.log.is_successful ? <CheckCircleTwoTone twoToneColor="#52c41a" /> : ('')}
              </Button>)
            }
            </Descriptions.Item>
            <Descriptions.Item>
              <Button onClick={()=>{
                delete_monitor(monitor.id)
              }} danger>
                Remove <CloseOutlined />
              </Button>
            </Descriptions.Item>
          </Descriptions>
        </Col>
        <Col>
          <Switch checkedChildren="On" unCheckedChildren="Off" onChange={TurnOn} checked={IsActive} />
        </Col>
        <Col span={8}>
          <Bar
            readings={BarMonitors}
            monitor={monitor}
          />
        </Col>
      </Row>
    </Card>
  );
}
