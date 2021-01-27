import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ChatComponent } from "./chat/chat.component";
import {AuthComponent} from "./auth/auth.component";

const routes: Routes = [
  { path: 'chat', component: ChatComponent, pathMatch: 'full'},
  { path: 'login', component: AuthComponent, pathMatch: 'full'},
  { path: '**', redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
