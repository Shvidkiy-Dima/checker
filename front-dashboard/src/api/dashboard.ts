import {AxiosPromise} from "axios";
import request from '../utils/request'
import {
	TResponseMonitors,
	IRequestAddMonitor,
	TResponseCreateMonitor,
	TResponseDisableMonitor,
	TResponseEnableTelegram
} from "../interfaces/dashboard";



export function ApiGetMonitors(){
    return request({
			method: 'get',
			url: `${process.env.REACT_APP_BASE_URL}/monitor/`,
			checkAuthorization: true,
			AuthorizationRequired: true
		}) as AxiosPromise<TResponseMonitors>;
}


export function ApiDisableMonitor(id: string, turn_off: boolean){
    return request({
			method: 'patch',
			url: `${process.env.REACT_APP_BASE_URL}/monitor/${id}/`,
			checkAuthorization: true,
			AuthorizationRequired: true,
			data: {is_active: turn_off},
		}) as AxiosPromise<TResponseDisableMonitor>;
}


export function ApiAddMonitor(data: IRequestAddMonitor){
    return request({
			method: 'post',
			url: `${process.env.REACT_APP_BASE_URL}/monitor/`,
			checkAuthorization: true,
			AuthorizationRequired: true,
			data,
		}) as AxiosPromise<TResponseCreateMonitor>;
}

export function ApiDeleteMonitor(id: string){
    return request({
			method: 'delete',
			url: `${process.env.REACT_APP_BASE_URL}/monitor/${id}/`,
			checkAuthorization: true,
			AuthorizationRequired: true,
		}) as AxiosPromise;
}


export function ApiEnableTelegram(){
    return request({
			method: 'post',
			url: `${process.env.REACT_APP_BASE_URL}/notification/telegram/`,
			checkAuthorization: true,
			AuthorizationRequired: true,
		}) as AxiosPromise<TResponseEnableTelegram>;
}