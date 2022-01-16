import React from "react";
import {
  Collapse,
  DropdownItem,
  DropdownMenu,
  DropdownToggle,
  Nav,
  Navbar,
  NavbarBrand,
  NavbarText,
  NavbarToggler,
  NavItem,
  NavLink,
} from "reactstrap";
import "bootstrap/dist/css/bootstrap.min.css";

export default function OurNavbar() {
  return (
    <nav class="navbar navbar-expand-sm navbar-light bg-light">
      <a class="navbar-brand" href="/">
        Aequitas Web
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="/aboutaequitas">
              About Aequitas
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/aequitasdocs">
              Aequitas Documentation
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/aboutus">
              About Us
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
}
