import {AxiosPromise} from "axios";
import request from '../utils/request'
import {IResponseProfile} from "../interfaces/profile";

export function ApiGetProfile(){

    return request({
			method: 'get',
			url: `${process.env.REACT_APP_BASE_URL}/account/profile/`,
			AuthorizationRequired: true,
		}) as AxiosPromise<IResponseProfile>;
}
