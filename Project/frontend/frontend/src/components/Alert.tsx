import React from "react";
import type { ReactNode } from "react";

interface AlertProps {
    children: ReactNode;
}

export const Alert = ({children}: AlertProps) => {
  return (
    <div className="alert alert-primary">
      {children}
    </div>
  );
};

export default Alert;
