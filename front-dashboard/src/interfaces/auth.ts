import {EAuthActions} from "../enums/actions.enum";

export interface ISetLoginAction {
    payload: Array<any>
    type: EAuthActions.SetLogin

}

export interface IRequestLogin {
    email: string
    password: string
}

export interface IRequestRegistration {
    email: string
    password: string
}


export interface IResponseLogin{
    token: string
}



export type TSetLoginAction = ISetLoginAction

