import React from "react";
import { Col, Row, Card, Spin} from "antd";
import request from '../../utils/request'


export default function RequireTelegram() { 
    const [TelegramLink, SetTelegramLink]  = React.useState(null)
    const [Load, ShowLoad] = React.useState(false)

    React.useEffect(()=>{
        request(
            { url: "api/notification/telegram/", method: "post" },
            (res) => {
              SetTelegramLink(res.data["deeplink"]);
            },
            (err) => {
                console.log(err)
            }
          );
    },
    [])


    function OpenLink(){
        ShowLoad(true)
        window.open(TelegramLink, '_blank').focus();
    }

    if (TelegramLink === null){
        return null
    }

    return (
        <div style={{ height: "100%", overflow: "hidden" }}>
        <Row justify="center">
          <Col>
            <Card
              title="We need enable Telegram notifications"
              bordered={false}
              style={{ width: 600, marginTop: "40%", textAlign: "center" }}
              headStyle={{
                textAlign: "center",
                fontSize: "2em",
                fontFamily: "Nunito",
              }}
            >
                      <p>Please follow link and start dialog with chat-bot. Link will be expired in 12 hours</p>
                      <a onClick={OpenLink}>{TelegramLink}</a>
                      <hr/>
                      {Load ? <Spin size="large" />: ''}
                      
            </Card>
          </Col>
       </Row>
      </div>
  
    )


}