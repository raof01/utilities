import { Injectable, Component } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { DbService } from './db.service';
import { Proxy } from '../proxy.service';
import { DbsComponent } from './dbs.component';

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
    private url: string = undefined;

    constructor(
        private dbService: DbService,
        private proxyService: Proxy
    ) {
        this.url = 'http://localhost:3000/';
        this.proxyService.subscribeDbSelected(this.onDbSelected.bind(this));
    }

    private onDbSelected(v: string) {
        console.log(v);
        this.dbService.getTables(this.url, this.serverIp, parseInt(this.serverPort), this.userName, this.password, v);
    }

    public onClick(event) {
        this.dbService.getDbs(this.url, this.serverIp, parseInt(this.serverPort), this.userName, this.password);
    }
}
