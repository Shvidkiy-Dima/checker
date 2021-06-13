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
  Statistic
} from "antd";
import {
  CheckCircleTwoTone,
  CloseOutlined,
} from "@ant-design/icons";
import "./monitor.css";
import request from "../../utils/request";
import Bar from "./bar";
import Timer from './timer'
import { Link } from "react-router-dom";
import convert_for_bar from '../../utils/methods'


export default function Monitor({ monitor, delete_monitor}) {

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

  let logs_data = React.useMemo(()=>convert_for_bar(monitor.log_groups, monitor.interval), [monitor.log.created])

  return (
    <Card style={{ width: "100%" }}>
      <Row gutter={16}>
        <Col span={8} style={{ marginRight: "4%" }}>
        <Link to={'/dashboard/' + monitor.id} style={{fontSize: '2em'}}>{ monitor.name }</Link>
        <br/>
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
            <Descriptions.Item label="interval">
                {monitor.interval_in_minutes} min

              <Button style={{marginLeft: '20%'}} onClick={()=>{
                delete_monitor(monitor.id)
              }} danger>
                Remove <CloseOutlined />
              </Button>
            </Descriptions.Item>
          </Descriptions>
        </Col>
        <Col span={8}>
          <Bar
            readings={logs_data}
            monitor={monitor}
          />
                  <Col>
          <Switch checkedChildren="On" unCheckedChildren="Off" onChange={TurnOn} checked={IsActive} />
        </Col>
        </Col>
      </Row>
    </Card>
  );
}
