import { Injectable, Component } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { DbService } from './db.service';
@Component({
    selector: 'db-login',
    templateUrl: './db-login.component.html',
    styleUrls: ['../app.component.css']
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

    constructor(
        private http: Http,
        private dbService: DbService
    ) {
    }

    onClick(event) {
        this.dbService.getDbs(this.serverIp, parseInt(this.serverPort), this.userName, this.password);
    }
}
