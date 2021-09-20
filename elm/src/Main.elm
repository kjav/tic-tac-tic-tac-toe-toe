module Main exposing (main)

import Browser
import Html exposing (Html, button, div, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import List.Extra as List



-- MAIN


main =
    Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
    { grid : Grid, rows : Int, cols : Int, activePlayer : Player }


type CellState
    = Empty
    | SelectedBy Player


type Player
    = PlayerX
    | PlayerO


type alias Grid =
    List (List CellState)


init : Model
init =
    let
        rows =
            3

        cols =
            3
    in
    { grid = emptyGrid rows cols
    , rows = rows
    , cols = cols
    , activePlayer = PlayerX
    }


emptyGrid : Int -> Int -> Grid
emptyGrid rows cols =
    List.repeat rows (List.repeat cols Empty)



-- UPDATE


type Msg
    = CellClicked ( Int, Int )


update : Msg -> Model -> Model
update msg model =
    case msg of
        CellClicked coord ->
            if isCellEmpty coord model.grid then
                clickCell coord model

            else
                model


togglePlayer : Player -> Player
togglePlayer player =
    case player of
        PlayerX ->
            PlayerO

        PlayerO ->
            PlayerX


clickCell : ( Int, Int ) -> Model -> Model
clickCell coord model =
    { model
        | grid =
            List.setAt (Tuple.first coord)
                (List.setAt (Tuple.second coord)
                    (SelectedBy model.activePlayer)
                    (Maybe.withDefault [] (List.getAt (Tuple.first coord) model.grid))
                )
                model.grid
        , activePlayer = togglePlayer model.activePlayer
    }



-- VIEW


view : Model -> Html Msg
view model =
    div [] [ viewBoard model.grid ]


viewBoard : Grid -> Html Msg
viewBoard boardState =
    div [] <|
        List.map
            (\n ->
                viewRow n
                    (List.getAt n boardState |> Maybe.withDefault [])
            )
            (List.range 0 (List.length boardState - 1))


viewRow : Int -> List CellState -> Html Msg
viewRow rowNum rowState =
    div [ style "display" "flex" ] <|
        List.map
            (\n ->
                viewCell ( rowNum, n )
                    (List.getAt n rowState
                        |> Maybe.withDefault Empty
                    )
            )
            (List.range 0 (List.length rowState - 1))


viewCell : ( Int, Int ) -> CellState -> Html Msg
viewCell coord cellState =
    let
        cellText =
            case cellState of
                Empty ->
                    "hello"

                SelectedBy PlayerO ->
                    "O"

                SelectedBy PlayerX ->
                    "X"
    in
    div []
        [ button
            [ onClick (CellClicked coord)
            , style "minHeight" "15px"
            ]
            [ text cellText ]
        ]



-- HELPERS


getCell : ( Int, Int ) -> Grid -> Maybe CellState
getCell coord grid =
    List.getAt (Tuple.first coord) grid
        |> Maybe.andThen (List.getAt (Tuple.second coord))


isCellEmpty : ( Int, Int ) -> Grid -> Bool
isCellEmpty coord grid =
    case getCell coord grid of
        Just Empty ->
            True

        _ ->
            False
