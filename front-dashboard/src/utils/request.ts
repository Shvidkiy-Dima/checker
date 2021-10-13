import axios, { AxiosError, AxiosRequestConfig } from 'axios';

import {EStatusCode} from '../enums/status_code.enum'
// import { store } from '../store/store';
//import { logout } from '../store/actions/profile';

interface IConfigFetch extends AxiosRequestConfig {
	errorCallback?: (error: AxiosError) => void;
	checkAuthorization?: boolean;
	AuthorizationRequired?: boolean;
}

export default async function Request(config: IConfigFetch) {
	let newConfig = { ...config };
	const { checkAuthorization = true, AuthorizationRequired } = config;
	const token: string | null = localStorage.getItem('token')
	if (AuthorizationRequired && token !== null) {
		newConfig = {
			...config,
			headers: {
				...config?.headers,
				Authorization: `Token ${token}`,
			},
		};
	}

	return axios(newConfig).catch((error: AxiosError) => {
		if (config.errorCallback) {
			config?.errorCallback?.(error);
		}
		if (checkAuthorization && error?.response?.status === EStatusCode.NOT_AUTHORIZED) {
				// logout()
		}
		throw error;
	});
}