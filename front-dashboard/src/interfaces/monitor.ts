import {ILastLog} from "./dashboard";
import {EMonitorActions} from "../enums/actions.enum";

export interface ISetMonitorAction {
    payload: IResponseDetailMonitor
    type: EMonitorActions.SetMonitor
}

export interface ISetNotFoundAction {
    payload: boolean
    type: EMonitorActions.SetNotFound
}


export interface IResponseDetailMonitor  {
  id: string,
  interval_in_minutes: number,
  url: string
  name: string,
  description: null | string,
  is_active: boolean,
  last_log: ILastLog | null,
  interval: string,
  next_request: string,
  successful_percent: number,
  unsuccessful_percent: number,
  last_request_in_seconds: number,
  created: number,
  error_notification_interval: number,
  error_notification_interval_in_minutes: number,
  by_telegram: boolean,
  by_email: boolean,
  max_timeout: string,
  avg_response_time: number,
  log_last_count: number,
  interval_logs: Array<any>,
  last_error_logs: Array<any>,
  log_groups: Array<any> | [],
  bar_data: Array<any>,
}


export type TMonitorAction = ISetMonitorAction | ISetNotFoundAction

