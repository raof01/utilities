import { Component } from '@angular/core';

@Component({
    selector: 'db-login',
    templateUrl: './db-login.component.html',
    styleUrls: ['./app.component.css']
})

/*
 * NOTE:
 * TODO: db-access logic should be in server side, instead of client side
 */
export class DbLoginComponent {
    title: string = 'Login';
    msg: string;
    serverIp: string;
    serverPort: string;
    userName: string;
    password: string;

    onClick(event) {
        this.msg = `${this.serverIp}:${this.serverPort}, ${this.userName}, ${this.password}`;
    }
}
