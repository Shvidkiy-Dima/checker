import {AxiosPromise} from "axios";
import request from '../utils/request'
import {IResponseDetailMonitor} from "../interfaces/monitor";


export function ApiGetMonitor(id: string){
    return request({
			method: 'get',
			url: `${process.env.REACT_APP_BASE_URL}/monitor/${id}/`,
			checkAuthorization: true,
			AuthorizationRequired: true
		}) as AxiosPromise<IResponseDetailMonitor>;
}

