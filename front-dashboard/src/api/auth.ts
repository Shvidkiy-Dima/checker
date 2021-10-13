import {AxiosPromise} from "axios";
import request from '../utils/request'
import {IResponseLogin, IRequestLogin, IRequestRegistration} from "../interfaces/auth";


export function ApiLogin(data: IRequestLogin){
    return request({
			method: 'post',
			url: `${process.env.REACT_APP_BASE_URL}/auth/sign-in/`,
            data
		}) as AxiosPromise<IResponseLogin>;
}

export function ApiLogout(){
    return request({
			method: 'delete',
			url: `${process.env.REACT_APP_BASE_URL}/auth/logout/`,
			checkAuthorization: true,
			AuthorizationRequired: true
		}) as AxiosPromise;
}


export function ApiRegistration(data: IRequestRegistration) {
	return request({
		method: 'post',
		url: `${process.env.REACT_APP_BASE_URL}/auth/sign-up/`,
		data
	}) as AxiosPromise;
}
