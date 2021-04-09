import React from "react";
import {
  HashRouter as Router,
  Switch,
  Route,
  Link,
  useParams,
  useRouteMatch,
} from "react-router-dom";
import {
  Layout,
  Col,
  Row,
  Card,
  Button,
  Checkbox,
  Slider,
  Descriptions,
} from "antd";
import request from "../../../utils/request";

export default function Config() {
  const [TelegramLink, SetTelegramLink] = React.useState(null);
  const [UserConfig, SetUserConfig] = React.useState(null);
  const [Telegram, SetTelegram] = React.useState(null);
  const [ErrorNotificationInterval, SetErrorNotificationInterval] = React.useState(null);

  function GetTelegram() {
    request(
      {
        url: "api/config/",
        method: "patch",
        data: { enable_telegram: !Telegram },
      },
      (res) => {
        let is_enabled = res.data["enable_telegram"];
        SetTelegram(is_enabled);
        if (is_enabled) {
          request(
            { url: "api/notification/telegram/", method: "post" },
            (res) => {
              let link = res.data["deeplink"];
              SetTelegramLink(link);
            },
            (err) => {}
          );
        }
      },
      (err) => {}
    );
  }

  function SaveConf(){
      let data = {error_notification_interval: ErrorNotificationInterval*60}
      request(
        {
          url: "api/config/",
          method: "patch",
          data: data,
        },
        (res)=>{
            SetErrorNotificationInterval(res.data.error_notification_interval)
        },
        (err)=>{
          console.log(err)
        }
      )
  }


  React.useEffect(() => {
    request(
      { url: "api/config/", method: "get" },
      (res) => {
        SetTelegram(res.data.enable_telegram);
        SetErrorNotificationInterval(res.data.error_notification_interval_in_minutes);
        SetUserConfig(res.data);
      },
      (err) => {
        console.log(err);
      }
    );
  }, []);
  if (!UserConfig) {
    return null;
  }

  return (
    <Layout.Content
      className="site-layout-background"
      style={{
        margin: "24px 16px",
        padding: 24,
        minHeight: 280,
      }}
    >
      <Card style={{ width: "100%" }}>
        <Row gutter={16}>
          <Col span={8} style={{ marginRight: "4%" }}>
            <Descriptions layout="vertical">
              <Descriptions.Item label="Telegram">
                <Checkbox checked={Telegram} onChange={GetTelegram}>
                  Checkbox
                </Checkbox>
              </Descriptions.Item>
            </Descriptions>
          </Col>
          {TelegramLink ? (
            <Col span={8}>
              <Descriptions layout="vertical">
                <Descriptions.Item label="Pleaase follow">
                  <Link to={TelegramLink}>{TelegramLink}</Link>
                </Descriptions.Item>
              </Descriptions>
            </Col>
          ) : (
            ""
          )}
        </Row>
      </Card>

      <Card style={{ width: "100%" }}>
        <Row gutter={16}>
          <Col span={8} style={{ marginRight: "4%" }}>
            Error
            <Slider
              min={5}
              max={20}
              defaultValue={ErrorNotificationInterval}
              disabled={false}
              onChange={(e) => {
                SetErrorNotificationInterval(e);
              }}
            />
          </Col>
        </Row>
      </Card>
      <Button size="large" type="primary" onClick={SaveConf} danger>
        Save
      </Button>
    </Layout.Content>
  );
}
