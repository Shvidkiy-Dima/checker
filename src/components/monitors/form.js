import React from "react";
import { Layout, Menu, Button, Modal, Slider, Form, Input } from "antd";
import request from "../../utils/request";


export default function MonitorForm({ show, setShow, SetMonitors, Monitors }) {
  const [MonitorType, setMonitorType] = React.useState(null);
  const [interval, setInterval] = React.useState(5);
  const [url, setUrl] = React.useState("");
  const [name, setName] = React.useState("");
  const [confirmLoading, setConfirmLoading] = React.useState(false);

  const handleClose = () => setShow(false);

  const handleOk = () => {
    setConfirmLoading(true);
    console.log(name, url, interval)
    let MonitorType = 0
    let data = {
      monitor_type: MonitorType,
      interval: interval * 60,
      name,
      url,
    };
    request(
      { method: "post", url: "api/monitor/", data },
      (res) => {
        setConfirmLoading(false);
        setShow(false);
        let monitor = res.data;
        console.log(monitor);
        SetMonitors({ ...Monitors, [monitor.id]: monitor });

      },
      (err) => {
        console.log(err);
      }
    );
  };


  return (
      <Modal
        title="Title"
        visible={show}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleClose}
      >
        <Form>
          <Form.Item label="Name">
            <Input value={name} onChange={(e)=>{setName(e.target.value)}}/>
          </Form.Item>
          <Form.Item label="Url">
            <Input value={url} onChange={(e)=>{setUrl(e.target.value)}} />
          </Form.Item>
          <Form.Item label="Interval" name="size">
            <Slider min={1} max={60} defaultValue={interval} onChange={(e)=>{setInterval(e)}} disabled={false} />
          </Form.Item>
        </Form>
      </Modal>
  );
}
