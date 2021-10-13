import React from "react";
import {useDispatch, useSelector} from "react-redux";
import {Button, Layout, Menu, Row} from "antd";
import {
  NodeExpandOutlined,
  LineChartOutlined,
  PlusOutlined
} from "@ant-design/icons";
import "./../dashboard.css";
// import Config from "./config/config";
// import DetailMonitor from "./detail/detail";
import {getMonitorsAction, ShowModalAction} from "../../../store/actions/dashboard";
import {RootState} from "../../../store/rootReducer";
import Monitor from "./monitor";
import {IResponseMonitor} from "../../../interfaces/dashboard";
import AddMonitor from './add_monitor'
import Ws from '../../../utils/ws'


const {Sider, Content} = Layout;



export default function Monitors() {

  const dispatch = useDispatch()
  const monitors = useSelector((state: RootState)=>state.dashboard.monitors);



  console.log('dashboard', monitors.length)

  React.useEffect(()=>{
    dispatch(getMonitorsAction())
  },[])


  function SetShowModal(){
      dispatch(ShowModalAction())
  }


  return (
        <Content
      className="site-layout-background"
      style={{
        margin: "24px 16px",
        padding: 24,
        minHeight: 280,
      }}
    >

          <AddMonitor/>
      <div style={{ textAlign: "center", marginBottom: "2%" }}>
    <Button size="large" type="primary" onClick={SetShowModal} danger>
          <PlusOutlined />
          New monitor {monitors.length}/{10}
    </Button>
      </div>

      <Row gutter={[16, 16]} >
      {monitors.map((monitor: IResponseMonitor, key: any) => (
        <Monitor key={key} monitor={monitor} />
      ))}
      </Row>
    </Content>
  );
}
