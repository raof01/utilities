import { Injectable, Component } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';

@Component({
    selector: 'db-login',
    templateUrl: './db-login.component.html',
    styleUrls: ['./app.component.css']
})

/*
 * NOTE:
 * TODO: db-access logic should be in server side, instead of client side
 */
@Injectable()
export class DbLoginComponent {
    title: string = 'Login';
    msg: string;
    serverIp: string;
    serverPort: string;
    userName: string;
    password: string;

    constructor(private http: Http) {
        this.http = http;
    }

    onClick(event) {
        let url: string = 'http://localhost:3000/dbs';
        let body: string = `{
            host: ${this.serverIp},
            port: ${parseInt(this.serverPort)},
            user: ${this.userName},
            password: ${this.password}
        }`;
        let query: string =
            `host=${this.serverIp}&port=${parseInt(this.serverPort)}&user=${this.userName}&password=${this.password}`;
        this.http.get(`${url}?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            console.log(value.json());
            this.msg = '\n' + value.json();
        });
        /*this.http.post(url, body, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            console.log(value);
        });*/
    }
}
