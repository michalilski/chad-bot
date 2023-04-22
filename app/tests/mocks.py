from typing import Any, Dict, List

from app.core.chat.chatgpt_handler import ChatGPTHandler


class ChatGPTMockHandler(ChatGPTHandler):
    def __init__(self):
        pass

    def request(self, prompt: str) -> str:
        return f"[ChatGPT response] {prompt}"


search_engine_mock_data: List[Dict[str, Any]] = [
    {
        "name": "Maciej",
        "surname": "Piasecki",
        "organization": "Wroclaw University of Science and Technology",
        "projects": ["CLARIN", "PL-WORDNET"],
        "research_interests": [
            "Computational Linguistics",
            "Natural Language Processing",
            "Human-Computer Interaction",
            "Artificial Intelligence",
            "Language Technology",
        ],
        "abstracts": [
            "A language without a wordnet is at a severe disadvantage. If this sounds outlandish to you, reconsider. Language technology is a signature area of computing on/for/around the Internet, a growing source of texts for all manner of automated processing, including increasingly clever search engines and more and more adequate machine translation. A wordnet–a rich repository of knowledge about words–is a key element of many a successful text processing or language processing application. The English WordNet, whose origins date back almost a quarter century, is the exemplar. It has become central to much work in Natural Language Processing. Wordnets for other languages have been in development since the mid-1990s, and new projects start every year. We report on the initial stages of a long-term project to create a similar resource for Polish. We have envisaged–though not quite achieved–a book for many audiences. The most immediate “clientele” are people who work with wordnets and on wordnets. We have attempted, without being too theoretical, to make our experience with one language approachable to people who need not know anything about that language. Computing professionals who work with Polish texts may find the technical discussion interesting; we have presented a variety of tools which allow fairly deep analyses of meaning, given enough text to work with. Linguists who use computers in their study–and rely on well-organised language resources–may be encouraged to acquire yet another element of their research workbench.",
            "A large number of different tags, limited corpora and the free word order are the main causes of low accuracy of tagging in Polish (automatic disambiguation of morphological descriptions) by applying commonly used techniques based on stochastic modelling. In the paper the rule-based architecture of the TaKIPI Polish tagger combining handwritten and automatically extracted rules is presented. The possibilities of optimisation of its parameters and component are discussed, including the possibility of using different methods of rules extraction, than C4. 5 Decision Trees applied initially. The main goal of this paper is to explore a range of promising rule-based classifiers and investigate their impact on the accuracy of tagging. Simple techniques of combing classifiers are also tested. The performed experiments have shown that even a simple combination of different classifiers can increase the tagger’s accuracy by almost one percent.",
        ],
        "languages": ["polish", "english"],
    },
    {
        "name": "Piotr",
        "surname": "Szymański",
        "organization": "Wroclaw University of Science and Technology",
        "projects": ["Maps123"],
        "research_interests": [
            "Urban Data",
            "Multi-Label Classification",
            "Spoken Language Understanding",
            "Natural Language Processing",
            "Artificial Intelligence",
        ],
        "abstracts": [
            "The scikit-multilearn is a Python library for performing multi-label classification. It is compatible with the scikit-learn and scipy ecosystems and uses sparse matrices for all internal operations; provides native Python implementations of popular multi-label classification methods alongside a novel framework for label space partitioning and division and includes modern algorithm adaptation methods, network-based label space division approaches, which extracts label dependency information and multi-label embedding classifiers. The library provides Python wrapped access to the extensive multi-label method stack from Java libraries and makes it possible to extend deep learning single-label methods for multi-label tasks. The library allows multi-label stratification and data set management. The implementation is more efficient in problem transformation than other established libraries, has good test coverage and follows PEP8. Source code and documentation can be downloaded from http://scikit. ml and also via pip. The project is BSD-licensed.",
            "We present a new approach to stratifying multi-label data for classification purposes based on the iterative stratification approach proposed by Sechidis et. al. in an ECML PKDD 2011 paper. Our method extends the iterative approach to take into account second-order relationships between labels. Obtained results are evaluated using statistical properties of obtained strata as presented by Sechidis. We also propose new statistical measures relevant to second-order quality: label pairs distribution, the percentage of label pairs without positive evidence in folds and label pair-fold pairs that have no positive evidence for the label pair. We verify the impact of new methods on classification performance of Binary Relevance, Label Powerset and a fast greedy community detection based label space partitioning classifier. The proposed approach lowers the variance of classification quality, improves label pair oriented measures and example distribution while maintaining a competitive quality in label-oriented measures. We also witness an increase in stability of network characteristics.",
        ],
        "languages": ["polish", "english", "russian", "ukrainian"],
    },
    {
        "name": "Piotr",
        "surname": "Bródka",
        "organization": "Wroclaw University of Science and Technology",
        "projects": ["Network123"],
        "research_interests": [
            "Network Science",
            "Data Science",
            "Spreading Processes",
            "Multilayer Networks",
            "Artificial Intelligence",
        ],
        "abstracts": [
            "The continuous interest in the social network area contributes to the fast development of this field. The new possibilities of obtaining and storing data facilitate deeper analysis of the entire network, extracted social groups and single individuals as well. One of the most interesting research topic is the dynamics of social groups which means analysis of group evolution over time. Having appropriate knowledge and methods for dynamic analysis, one may attempt to predict the future of the group, and then manage it properly in order to achieve or change this predicted future according to specific needs. Such ability would be a powerful tool in the hands of human resource managers, personnel recruitment, marketing, etc. The social group evolution consists of individual events and seven types of such changes have been identified in the paper: continuing, shrinking, growing, splitting, merging, dissolving.",
            "Influential users play an important role in online social networks since users tend to have an impact on one other. Therefore, the proposed work analyzes users and their behavior in order to identify influential users and predict user participation. Normally, the success of a social media site is dependent on the activity level of the participating users. For both online social networking sites and individual users, it is of interest to find out if a topic will be interesting or not. In this article, we propose association learning to detect relationships between users. In order to verify the findings, several experiments were executed based on social network analysis, in which the most influential users identified from association rule learning were compared to the results from Degree Centrality and Page Rank Centrality. The results clearly indicate that it is possible to identify the most influential users using association rule learning. In addition, the results also indicate a lower execution time compared to state-of-the-art methods.",
        ],
        "languages": ["polish", "english"],
    },
]
