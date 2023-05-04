(ns backend.core
  (:require [ring.middleware.reload :refer [wrap-reload]]
            [ring.adapter.jetty :refer [run-jetty]]
            [ring.util.response :refer [response]]))

(defn handler [request]
  (response (str request)))

(def app
  (wrap-reload #'handler))

(defn -main []
  (run-jetty app {:port 3000}))
