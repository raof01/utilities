import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { DbLoginComponent } from './db/db-login.component';
import { DbsComponent } from './db/dbs.component';
import { DbService } from './db/db.service';
import { Proxy } from './proxy.service';
import { RowsComponent } from './rows.component';

@NgModule({
  declarations: [
    AppComponent,
    DbLoginComponent,
    DbsComponent,
    RowsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [DbService, Proxy],
  bootstrap: [AppComponent]
})
export class AppModule { }
