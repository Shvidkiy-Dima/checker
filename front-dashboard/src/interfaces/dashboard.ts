import {EDashboardActions} from "../enums/actions.enum";
import {Id} from "@reduxjs/toolkit/dist/query/tsHelpers";

export interface ISetMonitorsAction {
    payload: Array<any>
    type: EDashboardActions.SetMonitors
}

export interface IUpdateMonitorAction {
    payload: IResponseMonitor
    type: EDashboardActions.UpdateMonitor
}

export interface IAddMonitorAction {
    payload: IResponseMonitor
    type: EDashboardActions.AddMonitor
}

export interface IDeleteMonitorAction {
    payload: string
    type: EDashboardActions.DeleteMonitor
}

export interface IShowModalAction {
    payload: any
    type: EDashboardActions.ShowModal
}


export interface IRequestAddMonitor {
      interval: number,
      error_notification_interval: number,
      max_timeout: number,
      by_telegram: boolean,
      by_email: boolean,
      name: string
      url: string
}


export interface ILastLog {
       response_code: number,
       response_time: number,
       is_successful: boolean,
       error: string,
       created: string
}

export interface IResponseMonitor {
     id: string,
     interval_in_minutes: number,
     url: string,
     name: string,
     is_active: boolean,
     interval: string,
     next_request: string,
     successful_percent: number,
     unsuccessful_percent: number,
     last_request_in_seconds: number,
     created: string,
     error_notification_interval: string,
     error_notification_interval_in_minutes: number,
     by_telegram: boolean,
     by_email: boolean,
     max_timeout: string,
    avg_response_time: null | number,
    log_last_count: number
}


export type TResponseDisableMonitor = {
    is_active: boolean
}

export type TResponseEnableTelegram = {
    deeplink: string
}

export type TResponseCreateMonitor = IResponseMonitor


export type TResponseMonitors = IResponseMonitor[]
export type TMonitorsAction = ISetMonitorsAction | IUpdateMonitorAction |
    IAddMonitorAction | IShowModalAction | IDeleteMonitorAction

