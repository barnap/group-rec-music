import sys

sys.path.append('../')

# TODO For demonstration purposes, for now we return only one recommendation and explanation!
def generate_survey_json_html(recommendations, explanations):
    intro_html = "<article class='intro'>    <h1 class='intro__heading intro__heading--income title'>                     Welcome              </h1>    <div class='intro__body wysiwyg'>       <p>In this survey, you will be shown a set of recommendations generated for your group.</p>       " \
                "<p>Based on the recommended song and the explanation, please complete the survey.        </div> </article>"

    rec_html = "<section> <div class='container'> <div class='row align-items-center'>" \
               "<div class='col-lg-6'><div class='p-5'>" \
               "<iframe src='" + recommendations[0] + "' width='300' height='380' frameborder='0' " \
                                                       "allowtransparency='true'></iframe></div></div> " \
                                                       "<div class='col-lg-6'><div class='p-5'><h3>" + explanations[
                   0] + \
               "</h3></div></div></div></div></section>"

    return intro_html, rec_html
