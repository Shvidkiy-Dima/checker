import React from "react";
import { Popover, Modal, Slider, Form, Input, Alert, Switch, Spin } from "antd";

import {InfoCircleOutlined} from "@ant-design/icons";

import {useDispatch, useSelector} from "react-redux";
import {AddMonitorAction, ShowModalAction} from '../../../store/actions/dashboard'
import {IRequestAddMonitor} from "../../../interfaces/dashboard";
import {ApiAddMonitor, ApiEnableTelegram} from "../../../api/dashboard";
import {RootState} from "../../../store/rootReducer";
import {SetTelegramAction} from "../../../store/actions/profile";

export default React.memo(function AddMonitor() {

  console.log('Modal')

  const has_telegram = useSelector((state: RootState)=>state.profile.has_telegram)
  const WsConnection = useSelector((state: RootState)=>state.profile.ws)
  console.log(has_telegram)
  const ShowModal = useSelector((state: RootState)=>state.dashboard.ShowModal)

  const dispatch = useDispatch()

  const [Interval, SetInterval] = React.useState(5);
  const [MaxTimeout, setMaxTimeout] = React.useState(10);
  const [ErrorInterval, setErrorInterval] = React.useState(5);
  const [Url, setUrl] = React.useState("");
  const [Name, setName] = React.useState("");
  const [ConfirmLoading, setConfirmLoading] = React.useState(false);

  const [EnabledEmail, SetEnabledEmail] = React.useState(true)
  const [EnabledTelegram, SetEnabledTelegram] = React.useState(false);
  const [WaitingTelegram, SetWaitingTelegram] = React.useState(false)

  const [NameError, SetNameError] = React.useState('')
  const [UrlError, SetUrlError] = React.useState('')
  const [CommonErrors, SetCommonErrors] = React.useState([])
  const [TelegramLink, SetTelegramLink] = React.useState<null|string>(null)

  async function enableTelegram(){
      const {data} = await ApiEnableTelegram()
      SetTelegramLink(data.deeplink)
  }

  function WaitTelegram(){
      SetWaitingTelegram(true)
      WsConnection.dispatch.telegram_response = ()=>{
        dispatch(SetTelegramAction(true))
        SetWaitingTelegram(false)
      }
  }

  function handleClose() {
    dispatch(ShowModalAction())
  }

  async function handleOk () {
    setConfirmLoading(true);

    const request_data: IRequestAddMonitor = {
      interval: Interval * 60,
      error_notification_interval: ErrorInterval * 60,
      max_timeout: MaxTimeout,
      by_telegram: EnabledTelegram,
      by_email: EnabledEmail,
      name: Name,
      url: Url,
    };

    try {
        const {data} = await ApiAddMonitor(request_data)
        setConfirmLoading(false);
        dispatch(AddMonitorAction(data))
    }
    catch (err: any){
      setConfirmLoading(false);
      if (err.response){
          SetNameError(err.response.data.name || '')
          SetUrlError(err.response.data.url || '')
          SetCommonErrors(err.response.data.non_field_errors || [])
        }
    }
  }
  console.log(CommonErrors, "COm")
  return (
      <Modal
        title="Title"
        visible={ShowModal}
        onOk={handleOk}
        confirmLoading={ConfirmLoading}
        onCancel={handleClose}
      >
        {WaitingTelegram ?
              <Spin tip="Wait telegram...">
            </Spin>
          :
               <Form>
          <Form.Item>
            Name
            <Input value={Name} onChange={(e)=>{setName(e.target.value)}}/>
            {NameError ? <Alert message={NameError} type="error"  />: ""}
          </Form.Item>
          <Form.Item>
            Url
            <Input value={Url} onChange={(e)=>{setUrl(e.target.value)}} />
            {UrlError ? <Alert message={UrlError} type="error"  />: ""}
          </Form.Item>
          <Form.Item name="size">
          <Popover placement="topLeft" content={'Interval beetwen error messages'}>
          <InfoCircleOutlined/> Error notification interval
          </Popover>
            <Slider min={1} max={60} defaultValue={ErrorInterval} onChange={(e)=>{setErrorInterval(e)}} disabled={false} />
          </Form.Item>

          <Popover placement="topLeft" content={'How often we will check your monitor'}>
          <InfoCircleOutlined/> Check interval
          </Popover>
          <Form.Item name="size">
            <Slider min={1} max={60} defaultValue={Interval} onChange={(e)=>{SetInterval(e)}} disabled={false} />
          </Form.Item>

          <Popover placement="topLeft" content={'Max timeout per request'}>
          <InfoCircleOutlined/> Request timeout
          </Popover>
          <Form.Item name="timeout">
            <Slider min={1} max={30} defaultValue={MaxTimeout} onChange={(e)=>{setMaxTimeout(e)}} disabled={false} />
          </Form.Item>


          <p>
          Notifications
          </p>
          <Form.Item name="size">
            <div style={{display: 'flex'}}>
            <p style={{marginRight: '5%'}}>TELEGRAM </p>
            {has_telegram ?

            <Switch onChange={()=>{SetEnabledTelegram(true)}} />
            :
            <>
              <Switch disabled/>
              <Alert message="You must enable telegram" banner />
              <button onClick={enableTelegram}>Enable</button>
              {TelegramLink ? <a href={TelegramLink} target='_blank' onClick={WaitTelegram}>{TelegramLink}</a>: null}
            </>
            }
            </div>
          </Form.Item>
          <Form.Item name="size">
          <div style={{display: 'flex'}}>
            <p style={{marginRight: '5%'}}>EMAIL </p>
            <Switch checked={EnabledEmail} onChange={()=>{SetEnabledEmail(!EnabledEmail)}} />
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
          }
      </Modal>
  );
}
)