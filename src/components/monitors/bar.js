import React from "react";
import "./monitor.css";
import { Tooltip } from "antd";
import Moment from 'react-moment';


export default function MultiColorProgressBar({ readings, monitor }) {

  console.log(readings)
  const [Value, SetValue] = React.useState('')
  const [ResCode, setResCode] = React.useState('')
  const [ResError, setResErro] = React.useState(null)


  let bars = readings.map(function (item, i) {
    if (item.value > 0) {
      return (
        <div
          onMouseEnter={() => {
            SetValue(item['created']);
            setResCode(item['res_code'])
            setResErro(item['error'])

          }}
          className="bar"
          style={{ backgroundColor: item.color, width: item.value + "%" }}
          key={i}
        >

        </div>
      );
    }
  });


  return (
    <div className="multicolor-bar">
        <Tooltip title={(<div>
          <Moment format='MMMM Do YYYY, h:mm:ss a'>{Value}</Moment>
          <p>{ResCode}</p>
          <p>{ResError}</p>
          </div>)}>
        <div className="bars">{bars == "" ? "" : bars}</div>
        </Tooltip>
        <div className="legends">
          <div className="legend">
            <span className="dot" style={{ color: "green" }}>
              ●
            </span>
            <span className="label">{monitor.successful_percent}%</span>
          </div>
          <div className="legend">
            <span className="dot" style={{ color: "red" }}>
              ●
            </span>
            <span className="label">{monitor.unsuccessful_percent}%</span>
          </div>
        </div>
    </div>
  );
}
