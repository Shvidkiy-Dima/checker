import React from "react";
import { Popover, Modal, Slider, Form, Input, Alert, Switch } from "antd";
import request from "../../utils/request";


export default function MonitorForm({ show, setShow, SetMonitors, Monitors, user }) {
  const [MonitorType, setMonitorType] = React.useState(null);
  const [interval, setInterval] = React.useState(5);
  const [Errorinterval, setErrorInterval] = React.useState(5);
  const [url, setUrl] = React.useState("");
  const [name, setName] = React.useState("");
  const [confirmLoading, setConfirmLoading] = React.useState(false);

  const [EnabledTelegram, SetEnabledTelegram] = React.useState(user.has_telegram);


  const [NameError, SetNameError] = React.useState('')
  const [UrlError, SetUrlError] = React.useState('')
  const [CommonErrors, SetCommonErrors] = React.useState([])
  const handleClose = () => setShow(false);

  const handleOk = () => {
    setConfirmLoading(true);
    let MonitorType = 0
    let data = {
      monitor_type: MonitorType,
      interval: interval * 60,
      error_notification_interval: Errorinterval * 60,
      by_telegram: EnabledTelegram,
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
        SetMonitors({[monitor.id]: monitor, ...Monitors });

      },
      (err) => {
        setConfirmLoading(false);
        if (err.response){
          SetNameError(err.response.data.name || '')
          SetUrlError(err.response.data.url || '')  
          SetCommonErrors(err.response.data.non_field_errors || []) 
        }
 
      }
    );
  };

  console.log(CommonErrors, "COm")
  return (
      <Modal
        title="Title"
        visible={show}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleClose}
      >
        <Form>
          <Form.Item>
            Name
            <Input value={name} onChange={(e)=>{setName(e.target.value)}}/>
            {NameError ? <Alert message={NameError} type="error"  />: ""}
          </Form.Item>
          <Form.Item>
            Url
            <Input value={url} onChange={(e)=>{setUrl(e.target.value)}} />
            {UrlError ? <Alert message={UrlError} type="error"  />: ""}
          </Form.Item>
          <Form.Item name="size">
          <Popover placement="topLeft" content={'Interval beetwen error messages'}>
          Error notification interval
          </Popover>
            <Slider min={5} max={60} defaultValue={interval} onChange={(e)=>{setErrorInterval(e)}} disabled={false} />
          </Form.Item>

          <Popover placement="topLeft" content={'How often we will make requests'}>
          Interval
          </Popover>
          <Form.Item name="size">
            <Slider min={1} max={60} defaultValue={interval} onChange={(e)=>{setInterval(e)}} disabled={false} />
          </Form.Item>
          <Form.Item name="size">
            <div style={{display: 'flex'}}>
            <p style={{marginRight: '5%'}}>TELEGRAM </p>
            {user.has_telegram ? 
            
            <Switch defaultChecked onChange={()=>{SetEnabledTelegram(true)}} /> 
            : 
            <>
              <Switch disabled/>
              <Alert message="You must enable telegram on settings page" banner />
            </>
            }
            </div>
          </Form.Item>
          <Form.Item name="size">
          <div style={{display: 'flex'}}>
            <p style={{marginRight: '5%'}}>WHATSAPP </p>
            <Switch disabled/>
            </div>
          </Form.Item>
          <Form.Item name="size">
          <div style={{display: 'flex'}}>
            <p style={{marginRight: '5%'}}>PHONE </p>
            <Switch disabled/>
            </div>
          </Form.Item>
          {CommonErrors.map((e, i)=><Alert message={e} type="error" key={i} />)}
        </Form>
      </Modal>
  );
}
