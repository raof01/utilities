import { Injectable, Component, Input } from '@angular/core';
import { Proxy } from './proxy.service';

@Component({
    selector: 'rows',
    templateUrl: './rows.component.html',
    styleUrls: ['./app.component.css']
})

/*
 * NOTE:
 * TODO: db-access logic should be in server side, instead of client side
 */
@Injectable()
export class RowsComponent {
    @Input()
    rows: any = undefined;
    private fields: string[] = undefined;

    constructor(private proxy: Proxy) {
        this.proxy.subscribeFields(this.onFieldsReceived.bind(this));
        this.proxy.subscribeRows(this.onRowsReceived.bind(this));
    }

    private onRowsReceived(v: any[]) {
        this.rows = v;
    }

    private onFieldsReceived(v: string[]) {
        this.fields = v;
    }
}
