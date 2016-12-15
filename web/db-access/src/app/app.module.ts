import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { DbLoginComponent } from './db/db-login.component';
import { DbsComponent } from './db/dbs.component';
import { DbService } from './db/db.service';
import { DbProxy } from './db/db.proxy';
import { RowsComponent } from './db/rows.component';
import { APP_STORES } from './app.store';

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
    HttpModule,
    APP_STORES
  ],
  providers: [DbService, DbProxy],
  bootstrap: [AppComponent]
})
export class AppModule { }
