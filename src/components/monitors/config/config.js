import React from "react";
import {
  Modal,
  Layout,
  Col,
  Row,
  Card,
  Button,
  Checkbox,
  Switch,
  Descriptions,
} from "antd";
import request from "../../../utils/request";

export default function Config() {
  const [TelegramLink, SetTelegramLink] = React.useState(null);
  const [TelegramEnabled, SetTelegramEnabled] = React.useState(null);
  const [TelegramLoading, SetTelegramLoading] = React.useState(false);

  const [UserConfig, SetUserConfig] = React.useState(null);

  function DoTelegram(value) {
    if (value === true) {
      request(
        { url: "api/notification/telegram/", method: "post" },
        (res) => {
          SetTelegramLoading(true);
          SetTelegramEnabled(true)
          let link = res.data["deeplink"];
          SetTelegramLink(link);
        },
        (err) => {}
      );
    }
    else if (value === false){
        request( { url: "api/notification/telegram/disable/", method: "post" },
        (res)=>{
            SetTelegramEnabled(false)
        },
        (err)=>{

        })
    }
  }

  React.useEffect(() => {
    request(
      { url: "api/config/", method: "get" },
      (res) => {
        SetTelegramEnabled(res.data.enable_telegram);
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
        minHeight: "100%",
      }}
    >
      <Modal
        title="Please follow link"
        visible={TelegramLink}
        footer={[
          <Button
            key="back"
            onClick={() => {
              SetTelegramLink(null);
            }}
          >
            Close
          </Button>,
        ]}
      >
        <a href={TelegramLink}>{TelegramLink}</a>
      </Modal>

      <Card style={{ width: "100%" }} title="Notifications">
        <Row gutter={16}>
          <Col span={8} style={{ marginRight: "4%" }}>
            <Descriptions layout="vertical">
              <Descriptions.Item label="Enable Telegram notifications">
                <Switch
                  loading={TelegramLoading}
                  checked={TelegramEnabled}
                  onChange={DoTelegram}
                />
              </Descriptions.Item>
            </Descriptions>
          </Col>
        </Row>
      </Card>
    </Layout.Content>
  );
}
